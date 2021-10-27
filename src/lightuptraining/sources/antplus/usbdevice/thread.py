import logging
from queue import Queue
from threading import Thread

import usb.core

from sources.antplus.usbdevice.protocols import Device

logger = logging.getLogger(__name__)


class USBThread(Thread):
    """
    Thread that reads from the USB device endpoint IN
    """

    def __init__(self, device: Device, read_size: int, queue: Queue):
        super().__init__()
        self.setDaemon(True)
        self.device = device
        self.endpoint_in = device.endpoint_in
        self.read_size = read_size
        self.message_queue = queue
        self._run = True

    def run(self) -> None:
        """
        Runs the thread and starts reading data
        """
        while self._run:
            try:
                data = self.endpoint_in.read(self.read_size)

                if not data:
                    logger.debug('received no data, stopping usb thread')
                    self.stop()
                    break

                logger.debug(f'read data from USB device: {data}')

                for byte in data:
                    self.message_queue.put(byte)

            except usb.core.USBError as e:
                if e.errno in [60, 110] and e.backend_error_code != -116:
                    # ignore these timeout errors
                    pass
                elif e.errno == 5:
                    logger.error('io error occurred, is the USB device still plugged in?')
                    self.stop()
                    self.device.close()
                    break
                else:
                    logger.error(f'USB error occurred: {e}')
                    self.stop()
                    self.device.close()
                    break

            except KeyboardInterrupt:
                self.message_queue.put(None)

        logger.debug('exiting USB read thread')
        self.message_queue.put(None)

        if self.device.is_open:
            self.device.close()

        return

    def stop(self) -> None:
        """
        Stops reading data
        """
        self._run = False
