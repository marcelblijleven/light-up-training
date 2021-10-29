from __future__ import annotations

import struct
from abc import ABC
from typing import List, Tuple

from lightuptraining.sources.antplus.messages import const
from lightuptraining.sources.antplus.messages.const import MESSAGE_OPEN_RX_SCAN_MODE, MESSAGE_RESET_SYSTEM
from lightuptraining.sources.antplus.messages.message import AbstractMessage, MessageData
from lightuptraining.sources.antplus.messages.util import (calculate_checksum, device_number_to_fields,
                                                           validate_device_number, validate_device_type,
                                                           set_pairing_bit_on_device_type)


class ConfigurationMessage(AbstractMessage, ABC):
    """
    Configuration messages are used to modify channels (assign, unassign, open, close)
    and configure them for required operations
    """
    message_id: int
    encoding_format: str
    content: List[int]

    @property
    def _message_without_checksum(self) -> Tuple[int, ...]:
        """
        Returns the entire message, but without the checksum.
        This can be used to calculate the checksum and validate the message
        """
        return (
            const.MESSAGE_SYNC, len(self.content), self.message_id, *self.content
        )

    @property
    def checksum(self) -> int:
        """
        Returns the checksum of the message, which is the XOR of all bytes in the message
        including the sync byte.
        """
        return calculate_checksum(self._message_without_checksum)

    def encode(self) -> bytes:
        """
        Uses the encoding format of the configuration message to pack the message into bytes
        """
        return struct.pack(self.encoding_format, *self.decode())

    def decode(self) -> Tuple[int, ...]:
        """
        Decodes the message into a Tuple of ints
        """
        return self._message_without_checksum + (self.checksum,)


class UnassignChannelMessage(ConfigurationMessage):
    """
    Message for unassigning a channel
    """
    message_id = const.MESSAGE_UNASSIGN_CHANNEL
    encoding_format = '<BBBBB'

    def __init__(self, channel_number: int):
        self.channel_number = channel_number
        self.content = [channel_number]

    @classmethod
    def _from_message(cls, message: MessageData):
        content = message.content
        return cls(*content)


class AssignChannelMessage(ConfigurationMessage):
    """
    Message for assigning a channel
    """
    message_id = const.MESSAGE_ASSIGN_CHANNEL
    encoding_format = '<BBBBBBB'

    def __init__(self, channel_number: int, channel_type: int, network_number: int):
        self.channel_number = channel_number
        self.content = [channel_number, channel_type, network_number]

    @classmethod
    def _from_message(cls, message: MessageData):
        content = message.content
        return cls(*content)


class CloseChannelMessage(ConfigurationMessage):
    """
    Message for closing a channel
    """
    message_id: int = const.MESSAGE_CLOSE_CHANNEL
    encoding_format = '<BBBBB'

    def __init__(self, channel_number: int):
        self.channel_number = channel_number
        self.content = [channel_number]

    @classmethod
    def _from_message(cls, message: MessageData):
        content = message.content
        return cls(*content)


class EnableExtendedMessagesMessage(ConfigurationMessage):
    """
    Enables receiving extended broadcast messages
    """
    message_id = const.MESSAGE_ENABLE_EXT_RX_MESSAGES
    encoding_format = '<BBBBBB'

    def __init__(self, enable: bool):
        filler = 0
        self.content = [filler, int(enable)]

    @classmethod
    def _from_message(cls, message: MessageData):
        content = message.content
        return cls(*content)


class OpenChannelMessage(ConfigurationMessage):
    """
    Message for opening a channel
    """
    message_id: int = const.MESSAGE_OPEN_CHANNEL
    encoding_format = '<BBBBB'

    def __init__(self, channel_number: int):
        self.channel_number = channel_number
        self.content = [channel_number]

    @classmethod
    def _from_message(cls, message: MessageData):
        content = message.content
        return cls(*content)


class OpenRxScanModeMessage(ConfigurationMessage):
    message_id: int = MESSAGE_OPEN_RX_SCAN_MODE
    encoding_format = '<BBBBB'

    def __init__(self, channel_number: int, synchronous_packages_only: bool = False):
        self.channel_number = channel_number
        if synchronous_packages_only:
            self.encoding_format = '<BBBBBB'
            self.content = [channel_number, int(synchronous_packages_only)]
        else:
            self.content = [channel_number]

    @classmethod
    def _from_message(cls, message: MessageData):
        content = message.content
        return cls(*content)


class SystemResetMessage(ConfigurationMessage):
    """
    Message for resetting the system
    """
    message_id: int = MESSAGE_RESET_SYSTEM
    encoding_format = '<BBBBB'

    def __init__(self):
        self.content = [0]

    @classmethod
    def _from_message(cls, message: MessageData):
        return cls()


class SetChannelIdMessage(ConfigurationMessage):
    """
    Message for setting channel id

    The device type is an 8 bit field, the most significant bit is the pairing bit

    The device number is a 16 bit field
    The provided device number is split into two bytes, for example if the number is 1000
    you first shift the number 8 places to the right (1000 >> 8) which leaves 0b11.
    You then use the XOR of the res
    """
    message_id: int = const.MESSAGE_CHANNEL_ID
    encoding_format: str = '<BBBBBBBBB'

    def __init__(self, channel_number: int, device_number: int, device_type: int, transmission_type: int,
                 set_pairing_bit: bool = True):
        validate_device_number(device_number)
        validate_device_type(device_type)

        device_number_fields = device_number_to_fields(device_number)
        device_type_with_pairing_bit = set_pairing_bit_on_device_type(device_type, set_pairing_bit)

        self.channel_number = channel_number
        self.content = [channel_number, *device_number_fields, device_type_with_pairing_bit, transmission_type]

    @classmethod
    def _from_message(cls, message: MessageData):
        content = message.content
        channel_number = content[0]
        device_number = (content[2] << 8) + content[1]  # LSB, so start with right most byte
        # device type contains pairing bit
        return cls(*content)


cim = SetChannelIdMessage.from_bytes(b'\xa4\x05Q\x01\xe8\x03\xf8\n\xe8')
print(cim.encode())
print(cim.encode() == b'\xa4\x05Q\x01\xe8\x03\xf8\n\xe8')


class SetChannelPeriodMessage(ConfigurationMessage):
    """
    Message for setting channel period
    """
    message_id: int = const.MESSAGE_CHANNEL_PERIOD
    encoding_format = '<BBBBBBB'

    def __init__(self, channel_number: int, channel_period: int):
        self.channel_number = channel_number
        content = bytearray([channel_number, ])
        content[1:3] = struct.pack("<H", channel_period)
        self.content = [byte for byte in content]

    @classmethod
    def _from_message(cls, message: MessageData):
        pass


class SetSearchTimeoutMessage(ConfigurationMessage):
    """
    Message for setting search timeout on the channel
    """
    message_id: int = const.MESSAGE_CHANNEL_SEARCH_TIMEOUT
    encoding_format = '<BBBBBB'

    def __init__(self, channel_number: int, timeout: int = 10):
        self.channel_number = channel_number
        self.content = [channel_number, timeout]

    @classmethod
    def _from_message(cls, message: MessageData):
        pass


class SetNetworkKeyMessage(ConfigurationMessage):
    """
    Message for setting network key on the channel
    """
    message_id: int = const.MESSAGE_SET_NETWORK_KEY
    encoding_format = '<BBBBBBBBBBBBB'

    def __init__(self, channel_number: int, network_key: List[int]):
        self.channel_number = channel_number
        self.content = [channel_number, *network_key]

    @classmethod
    def _from_message(cls, message: MessageData):
        pass


class SetRfFrequencyMessage(ConfigurationMessage):
    """
    Message for setting RF frequency for the channel
    """
    message_id: int = const.MESSAGE_CHANNEL_RF_FREQUENCY
    encoding_format = '<BBBBBB'

    def __init__(self, channel_number: int, rf_frequency: int):
        self.channel_number = channel_number
        self.content = [channel_number, rf_frequency]

    @classmethod
    def _from_message(cls, message: MessageData):
        pass


class SetTransmissionPowerMessage(ConfigurationMessage):
    """
    Message for setting transmit power on the channel
    """
    message_id: int = const.MESSAGE_SET_CHANNEL_TRANSMIT_POWER
    encoding_format = '<BBBBBB'

    def __init__(self, channel_number: int, transmit_power: int):
        if transmit_power < 0 or transmit_power > 4:
            raise ValueError("transmit power out of range")

        self.channel_number = channel_number
        self.content = [channel_number, transmit_power]

    @classmethod
    def _from_message(cls, message: MessageData):
        pass
