import logging
from queue import Queue
from threading import Thread
from typing import Union

import usb.core

from lightuptraining.sources.antplus.usbdevice.protocols import Device

logger = logging.getLogger(__name__)


class USBThread(Thread):
    """
    Thread that reads from the USB device endpoint IN
    """

    def __init__(self, device: Device, read_size: int, queue: Queue[Union[int, None]]):
        super().__init__()
        self.setDaemon(True)
        self.device = device
        self.endpoint_in = device.endpoint_in
        self.read_size = read_size
        self.message_queue = queue
        self._run = True

    def _handle_exception(self, e: usb.core.USBError) -> bool:
        """
        Handles the USBError thrown by the USB device while reading data.

        It will return True if operation can continue, and false if operation should be terminated.
        """
        if e.errno in [60, 110] and e.backend_error_code != -116:
            # ignore these timeout errors
            return True
        elif e.errno == 5:
            logger.error('io error occurred, is the USB device still plugged in?')
            self.stop()
            self.device.close()
            return False
        else:
            logger.error(f'USB error occurred: {e}')
            self.stop()
            self.device.close()
            return False

    def _try_read(self) -> bool:
        """
        Tries reading from the USB device. If data is read, it will be added to the message queue

        It will return True if operation can continue, and false if operation should be terminated.
        Any exception is allowed to bubble up to the run method
        """
        data = self.endpoint_in.read(self.read_size)

        if not data:
            logger.debug('received no data, stopping usb thread')
            self.stop()
            return False

        logger.debug(f'read data from USB device: {data}')

        for byte in data:
            self.message_queue.put(byte)

        return True

    def run(self) -> None:
        """
        Runs the thread and starts reading data
        """
        while self._run:
            try:
                if not self._try_read():
                    break
            except usb.core.USBError as e:
                if not self._handle_exception(e):
                    break

            except KeyboardInterrupt:
                break

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
