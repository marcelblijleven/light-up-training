import pytest

from lightuptraining.sources.antplus.usbdevice.device import USBDevice


@pytest.fixture()
def closed_usb_device() -> USBDevice:
    device = USBDevice(0x0001, 0x0002)
    device._is_open = False
    return device


@pytest.fixture()
def open_usb_device() -> USBDevice:
    device = USBDevice(0x0001, 0x0002)
    device._is_open = True
    return device
