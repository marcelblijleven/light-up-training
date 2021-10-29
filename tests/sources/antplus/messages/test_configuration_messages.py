import struct

import pytest

from lightuptraining.sources.antplus.messages.configuration_messages import UnassignChannelMessage, \
    AssignChannelMessage, CloseChannelMessage, EnableExtendedMessagesMessage, OpenChannelMessage, OpenRxScanModeMessage, \
    SystemResetMessage, SetChannelIdMessage, SetChannelPeriodMessage, SetSearchTimeoutMessage, SetNetworkKeyMessage, \
    SetRfFrequencyMessage, SetTransmissionPowerMessage
from lightuptraining.sources.antplus.messages.const import MESSAGE_SYNC, MESSAGE_UNASSIGN_CHANNEL, \
    MESSAGE_ASSIGN_CHANNEL, MESSAGE_CLOSE_CHANNEL, MESSAGE_ENABLE_EXT_RX_MESSAGES, MESSAGE_OPEN_CHANNEL, \
    MESSAGE_OPEN_RX_SCAN_MODE, MESSAGE_RESET_SYSTEM, MESSAGE_CHANNEL_ID, MESSAGE_CHANNEL_PERIOD, \
    MESSAGE_CHANNEL_SEARCH_TIMEOUT, MESSAGE_SET_NETWORK_KEY, MESSAGE_CHANNEL_RF_FREQUENCY, \
    MESSAGE_SET_CHANNEL_TRANSMIT_POWER
from lightuptraining.sources.antplus.profiles.const import DEVICE_TYPE_HEART_RATE


def test_unassign_channel_message():
    channel_number = 1
    expected_checksum = 229
    message = UnassignChannelMessage(channel_number)

    assert message.content == [channel_number]
    assert message.checksum == expected_checksum
    assert message.decode() == (MESSAGE_SYNC, 1, MESSAGE_UNASSIGN_CHANNEL, channel_number, expected_checksum)
    assert message.encode() == b'\xa4\x01A\x01\xe5'

    UnassignChannelMessage.from_bytes(b'\xa4\x01A\x01\xe5')


def test_assign_channel_message():
    channel_number = 1
    channel_type = 0x39
    network_number = 1
    expected_checksum = 220
    message = AssignChannelMessage(channel_number, channel_type, network_number)

    assert message.content == [channel_number, channel_type, network_number]
    assert message.checksum == expected_checksum
    assert message.decode() == (
        MESSAGE_SYNC, 3, MESSAGE_ASSIGN_CHANNEL, channel_number, channel_type, network_number, expected_checksum)
    assert message.encode() == b'\xa4\x03B\x019\x01\xdc'


def test_close_channel_message():
    channel_number = 1
    expected_checksum = 232
    message = CloseChannelMessage(channel_number)

    assert message.content == [channel_number]
    assert message.checksum == expected_checksum
    assert message.decode() == (MESSAGE_SYNC, 1, MESSAGE_CLOSE_CHANNEL, channel_number, expected_checksum)
    assert message.encode() == b'\xa4\x01L\x01\xe8'


def test_enable_extended_messages_message():
    filler = 0
    enable = True
    expected_checksum = 193
    message = EnableExtendedMessagesMessage(enable)

    assert message.content == [filler, int(enable)]
    assert message.checksum == expected_checksum
    assert message.decode() == (MESSAGE_SYNC, 2, MESSAGE_ENABLE_EXT_RX_MESSAGES, filler, int(enable), expected_checksum)
    assert message.encode() == b'\xa4\x02f\x00\x01\xc1'


def test_open_channel_message():
    channel_number = 1
    expected_checksum = 239
    message = OpenChannelMessage(channel_number)

    assert message.content == [channel_number]
    assert message.checksum == expected_checksum
    assert message.decode() == (MESSAGE_SYNC, 1, MESSAGE_OPEN_CHANNEL, channel_number, expected_checksum)
    assert message.encode() == b'\xa4\x01K\x01\xef'


def test_open_rx_scan_mode_message():
    channel_number = 1
    expected_checksum = 255
    message = OpenRxScanModeMessage(channel_number)

    assert message.content == [channel_number]
    assert message.checksum == expected_checksum
    assert message.decode() == (MESSAGE_SYNC, 1, MESSAGE_OPEN_RX_SCAN_MODE, channel_number, expected_checksum)
    assert message.encode() == b'\xa4\x01[\x01\xff'


def test_open_rx_scan_mode_message_synchronous_only():
    channel_number = 1
    expected_checksum = 253
    message = OpenRxScanModeMessage(channel_number, synchronous_packages_only=True)

    assert message.content == [channel_number, 1]
    assert message.checksum == expected_checksum
    assert message.decode() == (MESSAGE_SYNC, 2, MESSAGE_OPEN_RX_SCAN_MODE, channel_number, 1, expected_checksum)
    assert message.encode() == b'\xa4\x02[\x01\x01\xfd'


def test_system_reset_message():
    expected_checksum = 239
    message = SystemResetMessage()

    assert message.content == [0]
    assert message.checksum == expected_checksum
    assert message.decode() == (MESSAGE_SYNC, 1, MESSAGE_RESET_SYSTEM, 0, expected_checksum)
    assert message.encode() == b'\xa4\x01J\x00\xef'


def test_set_channel_id_message():
    channel_number = 1
    device_number = 1000
    device_type = DEVICE_TYPE_HEART_RATE
    transmission_type = 10
    expected_checksum = 232

    message = SetChannelIdMessage(channel_number, device_number, device_type, transmission_type)

    assert message.content == [channel_number, 232, 3, 248, transmission_type]
    assert message.checksum == expected_checksum
    assert message.decode() == (
        MESSAGE_SYNC, 5, MESSAGE_CHANNEL_ID, channel_number, 232, 3, 248, transmission_type, expected_checksum)
    assert message.encode() == b'\xa4\x05Q\x01\xe8\x03\xf8\n\xe8'


def test_set_channel_id_message_wildcards():
    channel_number = 1
    device_number = 0
    device_type = DEVICE_TYPE_HEART_RATE
    transmission_type = 0
    expected_checksum = 232

    message = SetChannelIdMessage(channel_number, device_number, device_type, transmission_type)

    assert message.content == [channel_number, 0, 0, 248, transmission_type]
    assert message.checksum == expected_checksum
    assert message.decode() == (
        MESSAGE_SYNC, 5, MESSAGE_CHANNEL_ID, channel_number, 232, 3, 248, transmission_type, expected_checksum)
    assert message.encode() == b'\xa4\x05Q\x01\xe8\x03\xf8\n\xe8'


def test_set_channel_period_message():
    channel_number = 1
    channel_period = 8070  # Two bytes
    channel_period_bytes = struct.pack('<H', channel_period)  # Two bytes
    expected_checksum = 124

    message = SetChannelPeriodMessage(channel_number, channel_period)

    assert message.content == [channel_number, *[byte for byte in channel_period_bytes]]
    assert message.checksum == expected_checksum
    assert message.decode() == (
        MESSAGE_SYNC, 3, MESSAGE_CHANNEL_PERIOD, channel_number, *[byte for byte in channel_period_bytes],
        expected_checksum)
    assert message.encode() == b'\xa4\x03C\x01\x86\x1f|'


def test_set_search_timeout_message():
    channel_number = 1
    timeout = 10
    expected_checksum = 233

    message = SetSearchTimeoutMessage(channel_number, timeout)

    assert message.content == [channel_number, timeout]
    assert message.checksum == expected_checksum
    assert message.decode() == (
        MESSAGE_SYNC, 2, MESSAGE_CHANNEL_SEARCH_TIMEOUT, channel_number, timeout, expected_checksum)
    assert message.encode() == b'\xa4\x02D\x01\n\xe9'


def test_set_network_key_message():
    channel_number = 1
    network_key = [255, 254, 1, 2, 3, 128, 120, 100]
    expected_checksum = 119

    message = SetNetworkKeyMessage(channel_number, network_key)

    assert message.content == [channel_number, *network_key]
    assert message.checksum == expected_checksum
    assert message.decode() == (
        MESSAGE_SYNC, 9, MESSAGE_SET_NETWORK_KEY, channel_number, *network_key, expected_checksum)
    assert message.encode() == b'\xa4\tF\x01\xff\xfe\x01\x02\x03\x80xdw'


def test_set_rf_frequency_message():
    channel_number = 1
    rf_frequency = 0x39
    expected_checksum = 219

    message = SetRfFrequencyMessage(channel_number, rf_frequency)

    assert message.content == [channel_number, rf_frequency]
    assert message.checksum == expected_checksum
    assert message.decode() == (
        MESSAGE_SYNC, 2, MESSAGE_CHANNEL_RF_FREQUENCY, channel_number, rf_frequency, expected_checksum)
    assert message.encode() == b'\xa4\x02E\x019\xdb'


def test_set_transmission_power_message():
    channel_number = 1
    tx_power = 1
    expected_checksum = 198

    message = SetTransmissionPowerMessage(channel_number, tx_power)

    assert message.content == [channel_number, tx_power]
    assert message.checksum == expected_checksum
    assert message.decode() == (
        MESSAGE_SYNC, 2, MESSAGE_SET_CHANNEL_TRANSMIT_POWER, channel_number, tx_power, expected_checksum)
    assert message.encode() == b'\xa4\x02`\x01\x01\xc6'


def test_set_transmission_power_message_power_out_of_range():
    channel_number = 1

    with pytest.raises(ValueError) as wrapped_e:
        SetTransmissionPowerMessage(channel_number, -1)

    assert 'transmit power out of range' in str(wrapped_e.value)

    with pytest.raises(ValueError) as wrapped_e:
        SetTransmissionPowerMessage(channel_number, 5)

    assert 'transmit power out of range' in str(wrapped_e.value)
