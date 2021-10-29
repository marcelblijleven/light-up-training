from queue import Queue
from typing import Union

import pytest_mock
import usb.core

from lightuptraining.sources.antplus.usbdevice.thread import USBThread


def test_usb_thread(mocker: pytest_mock.MockerFixture):
    mock_device = mocker.MagicMock()
    queue: Queue[Union[int, None]] = Queue()
    thread = USBThread(mock_device, 1, queue)

    # use side effect to return True the first iteration, and False the second time to break out of while loop
    mocked_try_read = mocker.patch.object(thread, '_try_read', side_effect=[True, False])

    thread.run()

    assert None in queue.queue
    assert mocked_try_read.call_count == 2
    mock_device.close.assert_called_once()


def test_usb_thread_usb_error(mocker: pytest_mock.MockerFixture):
    mock_device = mocker.MagicMock()
    queue: Queue[Union[int, None]] = Queue()
    thread = USBThread(mock_device, 1, queue)

    mock_err = usb.core.USBError('mock USB err', errno=1)

    # Raise exception from _try_read
    mocked_try_read = mocker.patch.object(thread, '_try_read', side_effect=mock_err)
    # Make _handle_exception return False to break out of while loop
    mocked_handle_exception = mocker.patch.object(thread, '_handle_exception', return_value=False)

    thread.run()

    assert None in queue.queue
    mocked_try_read.assert_called_once()
    mocked_handle_exception.assert_called_once_with(mock_err)
    mock_device.close.assert_called_once()


def test__handle_exception_timeout_error_errno60(mocker: pytest_mock.MockerFixture):
    mock_device = mocker.MagicMock()
    queue: Queue[Union[int, None]] = Queue()
    thread = USBThread(mock_device, 1, queue)
    mocked_stop = mocker.patch.object(thread, 'stop')

    mock_err_60 = usb.core.USBError('mock USB err', errno=60)

    assert thread._handle_exception(mock_err_60)
    mocked_stop.assert_not_called()
    mock_device.close.assert_not_called()


def test__handle_exception_timeout_error_errno110(mocker: pytest_mock.MockerFixture):
    mock_device = mocker.MagicMock()
    queue: Queue[Union[int, None]] = Queue()
    thread = USBThread(mock_device, 1, queue)
    mocked_stop = mocker.patch.object(thread, 'stop')

    mock_err_110 = usb.core.USBError('mock USB err', errno=110)

    assert thread._handle_exception(mock_err_110)
    mocked_stop.assert_not_called()
    mock_device.close.assert_not_called()


def test__handle_exception_timeout_error_errno59(mocker: pytest_mock.MockerFixture):
    mock_device = mocker.MagicMock()
    queue: Queue[Union[int, None]] = Queue()
    thread = USBThread(mock_device, 1, queue)
    mocked_stop = mocker.patch.object(thread, 'stop')

    mock_err_59 = usb.core.USBError('mock USB err', errno=59)

    assert not thread._handle_exception(mock_err_59)
    mocked_stop.assert_called_once()
    mock_device.close.assert_called_once()


def test__handle_exception_timeout_error_errno60_116(mocker: pytest_mock.MockerFixture):
    mock_device = mocker.MagicMock()
    queue: Queue[Union[int, None]] = Queue()
    thread = USBThread(mock_device, 1, queue)
    mocked_stop = mocker.patch.object(thread, 'stop')

    mock_err_60 = usb.core.USBError('mock USB err', errno=60)
    mock_err_60.backend_error_code = -116

    assert not thread._handle_exception(mock_err_60)
    mocked_stop.assert_called_once()
    mock_device.close.assert_called_once()


def test__handle_exception_timeout_error_errno110_116(mocker: pytest_mock.MockerFixture):
    mock_device = mocker.MagicMock()
    queue: Queue[Union[int, None]] = Queue()
    thread = USBThread(mock_device, 1, queue)
    mocked_stop = mocker.patch.object(thread, 'stop')

    mock_err_110 = usb.core.USBError('mock USB err', errno=110)
    mock_err_110.backend_error_code = -116

    assert not thread._handle_exception(mock_err_110)
    mocked_stop.assert_called_once()
    mock_device.close.assert_called_once()


def test__handle_exception_timeout_error_errno5(mocker: pytest_mock.MockerFixture):
    mock_device = mocker.MagicMock()
    queue: Queue[Union[int, None]] = Queue()
    thread = USBThread(mock_device, 1, queue)
    mocked_stop = mocker.patch.object(thread, 'stop')

    mock_err_5 = usb.core.USBError('mock USB err', errno=5)

    assert not thread._handle_exception(mock_err_5)
    mocked_stop.assert_called_once()
    mock_device.close.assert_called_once()


def test__handle_exception_io_error(mocker: pytest_mock.MockerFixture):
    mock_device = mocker.MagicMock()
    queue: Queue[Union[int, None]] = Queue()
    thread = USBThread(mock_device, 1, queue)
    mocked_stop = mocker.patch.object(thread, 'stop')

    mock_err_5 = usb.core.USBError('mock USB err', errno=5)

    assert not thread._handle_exception(mock_err_5)

    mocked_stop.assert_called_once()
    mock_device.close.assert_called_once()


def test__try_read(mocker: pytest_mock.MockerFixture):
    mock_device = mocker.MagicMock()
    queue: Queue[Union[int, None]] = Queue()
    thread = USBThread(mock_device, 1, queue)
    mocked_stop = mocker.patch.object(thread, 'stop')
    mocked_endpoint_in = mocker.patch.object(thread, 'endpoint_in')
    mocked_endpoint_in.read.return_value = [1, 2, 3]

    assert thread._try_read()
    assert queue.qsize() == 3
    assert queue.get_nowait() == 1
    assert queue.get_nowait() == 2
    assert queue.get_nowait() == 3

    mocked_stop.assert_not_called()


def test__try_read_no_data(mocker: pytest_mock.MockerFixture):
    mock_device = mocker.MagicMock()
    queue: Queue[Union[int, None]] = Queue()
    thread = USBThread(mock_device, 1, queue)
    mocked_stop = mocker.patch.object(thread, 'stop')
    mocked_endpoint_in = mocker.patch.object(thread, 'endpoint_in')
    mocked_endpoint_in.read.return_value = []

    assert not thread._try_read()
    assert queue.qsize() == 0

    mocked_stop.assert_called_once()


def test_stop(mocker: pytest_mock.MockerFixture):
    mock_device = mocker.MagicMock()
    queue: Queue[Union[int, None]] = Queue()
    thread = USBThread(mock_device, 1, queue)

    assert thread._run
    thread.stop()
    assert not thread._run
