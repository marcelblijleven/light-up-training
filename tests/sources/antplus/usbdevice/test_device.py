import platform

import pytest
import pytest_mock

from lightuptraining.sources.antplus.usbdevice.device import USBDevice
from lightuptraining.sources.antplus.usbdevice.exceptions import USBDeviceException


def test_init_device_not_found(mocker: pytest_mock.MockerFixture):
    mocker.patch('lightuptraining.sources.antplus.usbdevice.device.usb.core.find', return_value=None)

    with pytest.raises(USBDeviceException) as wrapped_e:
        USBDevice(0x01, 0x02)

    assert 'device not found' in str(wrapped_e.value)


def test_close(mocker: pytest_mock.MockerFixture, open_usb_device):
    mock_release_interface = mocker.patch('lightuptraining.sources.antplus.usbdevice.device.usb.util.release_interface')
    assert open_usb_device.is_open

    open_usb_device.close()

    open_usb_device._usb_read_thread.stop.assert_called_once()  # noqa
    mock_release_interface.assert_called_once()
    assert not open_usb_device.is_open


def test_close_already_closed(closed_usb_device):
    assert not closed_usb_device.is_open

    with pytest.raises(USBDeviceException) as wrapped_e:
        closed_usb_device.close()

    assert 'cannot close USB device, device is not open' in str(wrapped_e.value)


def test_open(mocked_usb_device):
    assert not mocked_usb_device.is_open
    mocked_usb_device.open()
    mocked_usb_device._usb_read_thread.start.assert_called_once()  # noqa
    assert mocked_usb_device.is_open


def test_open_already_opened(open_usb_device):
    assert open_usb_device.is_open

    with pytest.raises(USBDeviceException) as wrapped_e:
        open_usb_device.open()

    assert 'cannot open USB device, device is already open' in str(wrapped_e.value)


def test_write(open_usb_device):
    message = 'message'
    written = open_usb_device.write(message)
    assert len(message) == written


def test_write_closed_device(closed_usb_device):
    message = 'message'

    with pytest.raises(USBDeviceException) as wrapped_e:
        closed_usb_device.write(message)

    assert 'cannot write to device, device is closed' in str(wrapped_e.value)


def test__device_active_configuration(mocker: pytest_mock.MockerFixture, mocked_usb_device):
    mocked_get_active_configuration = mocker.patch.object(mocked_usb_device._device, 'get_active_configuration',
                                                          return_value=1)
    cfg = mocked_usb_device._device_active_configuration
    mocked_get_active_configuration.assert_called_once()
    assert cfg == 1


def test__device_active_configuration_device_not_configured(mocked_usb_device):
    mocked_usb_device._device = None

    with pytest.raises(USBDeviceException) as wrapped_e:
        _ = mocked_usb_device._device_active_configuration

    assert 'cannot get active configuration, no usb device configured' in str(wrapped_e.value)


def test__device_endpoint_in(mocker: pytest_mock.MockerFixture, mock_endpoint):
    mocker.patch('lightuptraining.sources.antplus.usbdevice.device.usb.core.find')
    mocker.patch('lightuptraining.sources.antplus.usbdevice.device.usb.util.find_descriptor',
                 return_value=mock_endpoint)

    device = USBDevice(0x01, 0x02)
    endpoint = device._device_endpoint_in

    assert endpoint == mock_endpoint


def test__device_endpoint_in_no_endpoint_found(mocker: pytest_mock.MockerFixture, mocked_usb_device):
    mocker.patch('lightuptraining.sources.antplus.usbdevice.device.usb.core.find')
    mocker.patch('lightuptraining.sources.antplus.usbdevice.device.usb.util.find_descriptor',
                 return_value=None)

    with pytest.raises(USBDeviceException) as wrapped_e:
        _ = mocked_usb_device._device_endpoint_in

    assert 'could not get endpoint with direction IN' in str(wrapped_e.value)


def test__device_endpoint_in_device_not_configured(mocked_usb_device):
    mocked_usb_device._device = None

    with pytest.raises(USBDeviceException) as wrapped_e:
        _ = mocked_usb_device._device_endpoint_in

    assert 'cannot get endpoint with direction IN, no usb device configured' in str(wrapped_e.value)


def test__device_endpoint_out(mocker: pytest_mock.MockerFixture, mock_endpoint):
    mocker.patch('lightuptraining.sources.antplus.usbdevice.device.usb.core.find')
    mocker.patch('lightuptraining.sources.antplus.usbdevice.device.usb.util.find_descriptor',
                 return_value=mock_endpoint)

    device = USBDevice(0x01, 0x02)
    endpoint = device._device_endpoint_out

    assert endpoint == mock_endpoint


def test__device_endpoint_out_no_endpoint_found(mocker: pytest_mock.MockerFixture, mocked_usb_device):
    mocker.patch('lightuptraining.sources.antplus.usbdevice.device.usb.core.find')
    mocker.patch('lightuptraining.sources.antplus.usbdevice.device.usb.util.find_descriptor',
                 return_value=None)

    with pytest.raises(USBDeviceException) as wrapped_e:
        _ = mocked_usb_device._device_endpoint_out

    assert 'could not get endpoint with direction OUT' in str(wrapped_e.value)


def test__device_endpoint_out_device_not_configured(mocked_usb_device):
    mocked_usb_device._device = None

    with pytest.raises(USBDeviceException) as wrapped_e:
        _ = mocked_usb_device._device_endpoint_out

    assert 'cannot get endpoint with direction OUT, no usb device configured' in str(wrapped_e.value)


def test__device_interface(mocker: pytest_mock.MockerFixture, mocked_usb_device):
    mocked_cfg = 'cfg'
    mocked_interface = 'interface'
    interface_number = 1

    mocked_active_cfg = mocker.patch(
        'lightuptraining.sources.antplus.usbdevice.device.USBDevice._device_active_configuration',
        new_callable=mocker.PropertyMock,
        return_value=mocked_cfg
    )
    mocked_interface_number = mocker.patch(
        'lightuptraining.sources.antplus.usbdevice.device.USBDevice._device_interface_number',
        new_callable=mocker.PropertyMock,
        return_value=interface_number)
    mocked_get_interface = mocker.patch(
        'lightuptraining.sources.antplus.usbdevice.device.usb.control.get_interface',
        return_value=mocked_interface
    )

    # Override existing patch from mocked_usb_device so we can assert the call
    mocked_find_descriptor = mocker.patch(
        'lightuptraining.sources.antplus.usbdevice.device.usb.util.find_descriptor'
    )

    # act
    _ = mocked_usb_device._device_interface

    mocked_active_cfg.assert_called_once()
    mocked_interface_number.assert_called_once()
    mocked_find_descriptor.assert_called_once_with(
        mocked_cfg, bInterfaceNumber=interface_number, bAlternateSetting=mocked_interface
    )
    mocked_get_interface.assert_called_once_with(mocked_usb_device._device, interface_number)


def test__device_interface_device_not_configured(mocked_usb_device):
    mocked_usb_device._device = None

    with pytest.raises(USBDeviceException) as wrapped_e:
        _ = mocked_usb_device._device_interface

    assert 'cannot get device interface, no USB device configured' in str(wrapped_e.value)


def test__device_interface_number(mocker: pytest_mock.MockerFixture, mocked_usb_device, mock_configuration):
    mocked_device_active_configuration = mocker.patch(
        'lightuptraining.sources.antplus.usbdevice.device.USBDevice._device_active_configuration',
        new_callable=mocker.PropertyMock,
        return_value=mock_configuration
    )

    interface_number = mocked_usb_device._device_interface_number
    mocked_device_active_configuration.assert_called_once()
    assert interface_number == 1


def test__device_interface_number_device_not_configured(mocked_usb_device):
    mocked_usb_device._device = None

    with pytest.raises(USBDeviceException) as wrapped_e:
        _ = mocked_usb_device._device_interface_number

    assert 'cannot get interface number, no USB device configured' in str(wrapped_e.value)


def test_endpoint_in(mocker: pytest_mock.MockerFixture, mocked_usb_device, mock_endpoint):
    mocked_device_endpoint_in = mocker.patch(
        'lightuptraining.sources.antplus.usbdevice.device.USBDevice._device_endpoint_in',
        new_callable=mocker.PropertyMock,
        return_value=mock_endpoint,
    )

    endpoint = mocked_usb_device.endpoint_in
    mocked_device_endpoint_in.assert_called_once()
    assert endpoint == mock_endpoint


def test_endpoint_out(mocker: pytest_mock.MockerFixture, mocked_usb_device, mock_endpoint):
    mocked_device_endpoint_out = mocker.patch(
        'lightuptraining.sources.antplus.usbdevice.device.USBDevice._device_endpoint_out',
        new_callable=mocker.PropertyMock,
        return_value=mock_endpoint,
    )

    endpoint = mocked_usb_device.endpoint_out
    mocked_device_endpoint_out.assert_called_once()
    assert endpoint == mock_endpoint


def test_is_open(mocked_usb_device):
    mocked_usb_device._is_open = False
    assert not mocked_usb_device.is_open

    mocked_usb_device._is_open = True
    assert mocked_usb_device.is_open


def test__configure_device(mocker: pytest_mock.MockerFixture):
    mocked_find = mocker.patch(
        'lightuptraining.sources.antplus.usbdevice.device.usb.core.find',
        return_value=mocker.MagicMock()
    )
    mocked_detach_kernel = mocker.patch(
        'lightuptraining.sources.antplus.usbdevice.device.USBDevice._device_detach_kernel',
        new_callable=mocker.PropertyMock
    )
    mocked_claim_interface = mocker.patch(
        'lightuptraining.sources.antplus.usbdevice.device.USBDevice._device_claim_interface',
        new_callable=mocker.PropertyMock
    )

    mocked_find_descriptor = mocker.patch(
        'lightuptraining.sources.antplus.usbdevice.device.usb.util.find_descriptor'
    )

    mocked_max_package_size = mocker.patch(
        'lightuptraining.sources.antplus.usbdevice.device.USBDevice._max_packet_size',
        return_value=0x40
    )

    device = USBDevice(0x01, 0x02)
    mocked_find_descriptor.assert_called()
    mocked_max_package_size.assert_called_once()
    mocked_find.assert_called_once()
    mocked_detach_kernel.assert_called_once()
    mocked_claim_interface.assert_called_once()
    device._device.set_configuration.assert_called_once()  # type: ignore # noqa


def test__device_claim_interface(mocker: pytest_mock.MockerFixture, mocked_usb_device):
    mocked_device_interface_number = mocker.patch(
        'lightuptraining.sources.antplus.usbdevice.device.USBDevice._device_interface_number',
        new_callable=mocker.PropertyMock,
        return_value=0x02
    )
    mocked_usb_util_claim_interface = mocker.patch(
        'lightuptraining.sources.antplus.usbdevice.device.usb.util.claim_interface',
    )

    mocked_usb_device._device_claim_interface()

    mocked_device_interface_number.assert_called_once()
    mocked_usb_util_claim_interface.assert_called_once_with(mocked_usb_device._device, 0x02)


@pytest.mark.skip()
@pytest.mark.skipif(platform.system() == 'Windows', reason='does not work on Windows')
def test__device_detach_kernel(mocker: pytest_mock.MockerFixture, mocked_usb_device):
    # figure out how to do the iteration of a mocked device / config
    pass


@pytest.mark.skipif(platform.system() != 'Windows', reason='Windows specific test')
def test__device_detach_kernel_on_windows(mocker: pytest_mock.MockerFixture, mocked_usb_device):
    mocked_detach_kernel = mocker.patch(
        'lightuptraining.sources.antplus.usbdevice.device.USBDevice._device_detach_kernel',
        new_callable=mocker.PropertyMock
    )

    mocked_usb_device._device_detach_kernel()
    # Should not call detach kernel on Windows because it is not implemented
    mocked_detach_kernel.assert_not_called()


def test__device_release_interface(mocker: pytest_mock.MockerFixture, mocked_usb_device):
    mocked_device_interface_number = mocker.patch(
        'lightuptraining.sources.antplus.usbdevice.device.USBDevice._device_interface_number',
        new_callable=mocker.PropertyMock,
        return_value=0x02
    )
    mocked_usb_util_release_interface = mocker.patch(
        'lightuptraining.sources.antplus.usbdevice.device.usb.util.release_interface',
    )

    mocked_usb_device._device_release_interface()

    mocked_device_interface_number.assert_called_once()
    mocked_usb_util_release_interface.assert_called_once_with(mocked_usb_device._device, 0x02)


def test__read(mocked_usb_device):
    mocked_usb_device.open()
    mocked_usb_device._message_queue.put_nowait(1)
    mocked_usb_device._message_queue.put_nowait(2)
    mocked_usb_device._message_queue.put_nowait(3)

    byte_1 = mocked_usb_device._read(1)
    byte_2 = mocked_usb_device._read(1)
    byte_3 = mocked_usb_device._read(1)

    assert byte_1 == b'\x01'
    assert byte_2 == b'\x02'
    assert byte_3 == b'\x03'


def test__read_multiple_bytes(mocked_usb_device):
    mocked_usb_device.open()
    mocked_usb_device._message_queue.put_nowait(1)
    mocked_usb_device._message_queue.put_nowait(2)
    mocked_usb_device._message_queue.put_nowait(3)

    byte_data = mocked_usb_device._read(3)

    assert byte_data == b'\x01\x02\x03'


def test__read_not_enough_bytes(mocked_usb_device):
    mocked_usb_device.open()
    mocked_usb_device._message_queue.put_nowait(1)
    mocked_usb_device._message_queue.put_nowait(2)
    mocked_usb_device._message_queue.put_nowait(3)

    byte_data = mocked_usb_device._read(4)

    assert byte_data == b''


def test__read_device_not_open(closed_usb_device):
    with pytest.raises(USBDeviceException) as wrapped_e:
        closed_usb_device._read(1)

    assert 'cannot read from device, device is closed' in str(wrapped_e.value)


def test__write(mocker: pytest_mock.MockerFixture, open_usb_device, mock_endpoint):
    mocker.patch(
        'lightuptraining.sources.antplus.usbdevice.device.USBDevice._device_endpoint_out',
        new_callable=mocker.PropertyMock,
        return_value=mock_endpoint
    )

    size = open_usb_device.write('abc', timeout=1)
    assert size == len('abc')


def test__write_device_not_open(closed_usb_device):
    with pytest.raises(USBDeviceException) as wrapped_e:
        closed_usb_device._write(bytes([1]))

    assert 'cannot write to device, device is closed' in str(wrapped_e.value)


@pytest.mark.skip()
def test_device_info():
    pass


def test_read(mocker: pytest_mock.MockerFixture, open_usb_device):
    mocked_read = mocker.patch.object(open_usb_device, '_read')
    _ = open_usb_device.read(3)
    mocked_read.assert_called_once_with(3, None)
