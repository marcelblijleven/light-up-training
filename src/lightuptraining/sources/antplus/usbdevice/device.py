from __future__ import annotations

import logging
from queue import Queue
from threading import Lock
from typing import Optional, Any, List, Union

import usb.control
import usb.core
import usb.util

from lightuptraining.protocols import Encodeable
from lightuptraining.sources.antplus.usbdevice.exceptions import USBDeviceException
from lightuptraining.sources.antplus.usbdevice.thread import USBThread

logger = logging.getLogger(__name__)


class USBDevice:
    """
    USBDevice reads serial data from a physical USB port and stores the data
    in a Queue until it is read
    """

    def __init__(self, vendor_id: int, product_id: int):
        self.vendor_id: int = vendor_id
        self.product_id: int = product_id

        self._device: Optional[usb.core.Device] = None
        self._is_open = False
        self._lock = Lock()
        self._message_queue: Queue[Union[int, None]] = Queue()
        self._configure_device()
        self._usb_read_thread = USBThread(self, self._max_packet_size(), self._message_queue)

    def __enter__(self) -> USBDevice:
        """
        Opens the USB device and returns the instance
        """
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Closes the USB device
        """

    def __rich__(self) -> str:
        return f'[blue]USB device ' \
               f'[yellow](vendor id: [red]{self.vendor_id:#0x}[/red] product id [red]{self.product_id:#0x}[/red])[/yellow])'

    def __str__(self) -> str:
        return f'USB device (vendor id: {self.vendor_id:#0x} product id {self.product_id:#0x})'

    @property
    def _device_active_configuration(self) -> Any:
        """
        Returns the currently active configuration
        """
        if not self._device:
            raise USBDeviceException(
                message='cannot get active configuration, no usb device configured',
                vendor_id=self.vendor_id,
                product_id=self.product_id,
            )

        return self._device.get_active_configuration()

    @property
    def _device_endpoint_in(self) -> usb.core.Endpoint:
        """
        Retrieves the endpoint with direction IN from the USB device
        """
        if not self._device:
            raise USBDeviceException(
                message='cannot get endpoint with direction IN, no usb device configured',
                vendor_id=self.vendor_id,
                product_id=self.product_id,
            )

        def match_func(e: usb.core.Endpoint) -> bool:
            return bool(usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN)

        endpoint = usb.util.find_descriptor(self._device_interface, custom_match=match_func)

        if not endpoint:
            raise USBDeviceException(
                message='could not get endpoint with direction IN',
                vendor_id=self.vendor_id,
                product_id=self.product_id,
            )

        return endpoint

    @property
    def _device_endpoint_out(self) -> usb.core.Endpoint:
        """
        Retrieves the endpoint with direction OUT from the USB device
        """
        if not self._device:
            raise USBDeviceException(
                message='cannot get endpoint with direction OUT, no usb device configured',
                vendor_id=self.vendor_id,
                product_id=self.product_id,
            )

        def match_func(e: usb.core.Endpoint) -> bool:
            return bool(usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT)

        endpoint = usb.util.find_descriptor(self._device_interface, custom_match=match_func)

        if not endpoint:
            raise USBDeviceException(
                message='could not get endpoint with direction OUT',
                vendor_id=self.vendor_id,
                product_id=self.product_id,
            )

        return endpoint

    @property
    def _device_interface(self):
        """
        Returns the device interface
        """
        if not self._device:
            raise USBDeviceException(
                message='cannot get device interface, no USB device configured',
                vendor_id=self.vendor_id,
                product_id=self.product_id,
            )

        cfg = self._device_active_configuration
        interface_number = self._device_interface_number

        return usb.util.find_descriptor(
            cfg,
            bInterfaceNumber=interface_number,
            bAlternateSetting=usb.control.get_interface(self._device, interface_number)
        )

    @property
    def _device_interface_number(self) -> int:
        """
        Returns the interface number of the currently active configuration
        """
        if not self._device:
            raise USBDeviceException(
                message='cannot get interface number, no USB device configured',
                vendor_id=self.vendor_id,
                product_id=self.product_id,
            )

        cfg = self._device_active_configuration
        return int(cfg[(0, 0)].bInterfaceNumber)

    @property
    def endpoint_in(self) -> usb.core.Endpoint:
        """
        Returns the endpoint with direction IN
        """
        return self._device_endpoint_in

    @property
    def endpoint_out(self) -> usb.core.Endpoint:
        """
        Returns the endpoint with direction OUT
        """
        return self._device_endpoint_out

    @property
    def is_open(self) -> bool:
        """
        Checks if the USB device is currently open
        """
        return self._is_open

    def _configure_device(self):
        """
        Finds and configures the USB device
        """
        device = usb.core.find(idVendor=self.vendor_id, idProduct=self.product_id)

        if not device:
            raise USBDeviceException(
                message='device not found',
                vendor_id=self.vendor_id,
                product_id=self.product_id,
            )

        self._device = device
        self._device_detach_kernel()
        self._device.set_configuration()
        self._device_claim_interface()

    def _device_claim_interface(self):
        """
        Claims the interface of the currently active configuration
        """
        # Figure out if this is actually necessary, pyusb docs mention it is
        # uncommon the explicitly call this method
        usb.util.claim_interface(self._device, self._device_interface_number)

    def _device_detach_kernel(self):
        """
        Detaches the kernel for all interfaces (only on Unix systems)
        """
        if not self._device:
            raise USBDeviceException(
                message='cannot detach kernel, device is not configured',
                vendor_id=self.vendor_id,
                product_id=self.product_id,
            )

        for cfg in self._device:
            for interface in cfg:
                try:
                    if self._device.is_kernel_driver_active(interface.index):
                        _detach_kernel(self, self._device, interface)
                except NotImplementedError:
                    pass  # NotImplementedError is raised on non Unix systems, so it can be ignored

    def _device_release_interface(self):
        """
        Releases the claimed interface of the currently active configuration
        """
        usb.util.release_interface(self._device, self._device_interface_number)

    def _max_packet_size(self):
        try:
            max_packet_size = self._device_endpoint_in.wMaxPacketSize
            logger.debug(f'max packet size read from device: {max_packet_size:#0x}')
        except AttributeError:
            max_packet_size = 0x40
            logger.debug(f'could not read max packet size from device, using default {max_packet_size:#0x}')

        return max_packet_size

    def _read(self, size: int, timeout: Optional[int] = None) -> bytes:
        """
        Read bytes from the message queue
        """
        if not self.is_open:
            raise USBDeviceException(
                message='cannot read from device, device is closed',
                vendor_id=self.vendor_id,
                product_id=self.product_id,
            )

        read_bytes: List[int] = []  # alternatively, use bytearray()

        if size > self._message_queue.qsize():
            logger.debug(f'not enough bytes in queue, tried to read {size} bytes')
            # Maybe raise an exception?
            return b""

        for i in range(size):
            byte = self._message_queue.get(timeout=timeout)

            if byte:
                read_bytes.append(byte)

        return bytes(read_bytes)

    def _write(self, data: bytes, timeout: Optional[int] = None) -> int:
        """
        Write bytes to the endpoint with direction OUT
        """
        if not self.is_open:
            raise USBDeviceException(
                message='cannot write to device, device is closed',
                vendor_id=self.vendor_id,
                product_id=self.product_id,
            )

        return int(self._device_endpoint_out.write(data, timeout))

    def close(self) -> None:
        """
        Closes the USB device
        """
        if not self.is_open:
            raise USBDeviceException(
                message='cannot close USB device, device is not open',
                vendor_id=self.vendor_id,
                product_id=self.product_id,
            )

        with self._lock:
            self._is_open = False
            self._device_release_interface()
            self._usb_read_thread.stop()
            logging.info("usb device closed")

    def device_info(self) -> str:
        """
        Get device info
        """
        if not self.is_open:
            return str(self)

        device: usb.core.Device = self._device
        info = [
            str(self),
            f'product: {device.product}',
            f'manufacturer: {device.manufacturer}',
            f'address: {device.address}',
            f'bus: {device.bus}',
            f'port number: {device.port_number}',
            f'speed: {device.speed}',
        ]

        return '\n'.join(info)

    def open(self) -> None:
        """
        Opens the USB device
        """
        if self.is_open:
            raise USBDeviceException(
                message='cannot open USB device, device is already open',
                vendor_id=self.vendor_id,
                product_id=self.product_id,
            )

        with self._lock:
            self._usb_read_thread.start()
            self._is_open = True
            logger.info('USB device opened')
            logger.info('\n' + self.device_info())

    def read(self, size: int, timeout: Optional[int] = None) -> bytes:
        """
        Reads bytes from the message queue
        """
        return self._read(size, timeout)

    def write(self, message: Encodeable, timeout: Optional[int] = None) -> int:
        """
        Writes the encodable message to the USB device and returns the amount of bytes written
        """
        return self._write(message.encode(), timeout)


def _detach_kernel(usb_device: USBDevice, device: usb.core.Device, interface: usb.core.Interface):
    try:
        device.detach_kernel_driver(interface.index)
        logger.debug(f'detached kernel driver for interface {interface.index}')
    except usb.core.USBError as e:
        raise USBDeviceException(
            message=f'failed to detach kernel driver for interface {interface.index}: {e}',
            vendor_id=usb_device.vendor_id,
            product_id=usb_device.product_id,
        )
