from typing import Optional, Generator
from unittest.mock import MagicMock

import pytest
import pytest_mock

from lightuptraining.sources.antplus.usbdevice.device import USBDevice


class MockConfigurationObject:
    def __init__(self, number: int):
        self.number = number

    @property
    def bInterfaceNumber(self) -> int:  # noqa
        return self.number


class MockConfiguration:
    def __init__(self):
        self.configurations = {
            (0, 0): MockConfigurationObject(1)
        }

    def __getitem__(self, item) -> MockConfigurationObject:
        return self.configurations[item]


class MockEndpoint:
    @property
    def wMaxPacketSize(self) -> int:  # noqa
        return 0x40

    def write(self, data: bytes, timeout: Optional[int] = None) -> int:
        return len(data)


class MockDevice:
    def __init__(self):
        self.product = 'mock USB device'
        self.manufacturer = 'happylife'
        self.address = 0x1000
        self.bus = 0x1000
        self.port_number = 0x01
        self.speed = 40

    def detach_kernel_driver(self):
        pass

    def get_active_configuration(self):
        pass

    def is_kernel_driver_active(self):
        pass

    def set_configuration(self):
        pass


@pytest.fixture()
def mock_endpoint():
    return MockEndpoint()


@pytest.fixture()
def mock_configuration():
    return MockConfiguration()


@pytest.fixture()
def mocked_usb_device(mocker: pytest_mock.MockerFixture) -> Generator[USBDevice, None, None]:
    with mocker.patch('lightuptraining.sources.antplus.usbdevice.device.usb.core.find'):
        with mocker.patch('lightuptraining.sources.antplus.usbdevice.device.usb.util.find_descriptor',
                          return_value=MockEndpoint()):
            with mocker.patch('lightuptraining.sources.antplus.usbdevice.device.USBThread',
                              return_value=MagicMock()):
                device = USBDevice(0x0001, 0x0002)
                yield device


@pytest.fixture()
def closed_usb_device(mocked_usb_device: USBDevice) -> USBDevice:
    mocked_usb_device._is_open = False
    return mocked_usb_device


@pytest.fixture()
def open_usb_device(mocked_usb_device: USBDevice) -> USBDevice:
    mocked_usb_device.open()
    mocked_usb_device._usb_read_thread.start.assert_called_once()  # type: ignore # noqa
    return mocked_usb_device
