from __future__ import annotations

import logging

from lightuptraining.sources.antplus.usbdevice.exceptions import USBDeviceException

logger = logging.getLogger(__name__)


class USBDevice:
    """
    USBDevice reads serial data from a physical USB port and stores the data
    in a Queue until it is read
    """

    def __init__(self, vendor_id: int, product_id: int):
        self.vendor_id: int = vendor_id
        self.product_id: int = product_id
        self._is_open = False

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
               f'[yellow](vendor id: [red]{self.vendor_id}[/red] product id [red]{self.product_id}[/red])[/yellow] '

    def __str__(self) -> str:
        return f'USB device (vendor id: {self.vendor_id} product id {self.product_id})'

    @property
    def is_open(self) -> bool:
        """
        Checks if the USB device is currently open
        """
        return self._is_open

    def open(self):
        """
        Opens the USB device
        """
        if self.is_open:
            raise USBDeviceException(
                message='cannot open USB device, device is already open',
                vendor_id=self.vendor_id,
                product_id=self.product_id,
            )

        self._is_open = True
