import pytest
import pytest_mock

from lightuptraining.sources.antplus.usbdevice.exceptions import USBDeviceException


def test_usbdevice_open(mocker: pytest_mock.MockerFixture, closed_usb_device):
    assert not closed_usb_device.is_open
    closed_usb_device.open()
    assert closed_usb_device.is_open


def test_usbdevice_open_already_opened(mocker: pytest_mock.MockerFixture, open_usb_device):
    assert open_usb_device.is_open

    with pytest.raises(USBDeviceException) as wrapped_e:
        open_usb_device.open()

    assert 'cannot open USB device, device is already open' in str(wrapped_e.value)
