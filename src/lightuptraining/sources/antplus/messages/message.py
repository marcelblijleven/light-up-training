import struct
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Type, TypeVar, Tuple

from lightuptraining.sources.antplus.messages.util import calculate_checksum

# This makes it possible to have type hinting for classmethods of child instances
# of the AbstractMessage
T = TypeVar('T', bound='AbstractMessage')


@dataclass
class MessageData:
    """
    Represents the content of a message, from the sync byte to the checksum
    """
    sync: int
    length: int
    message_id: int
    content: Tuple[int]
    checksum: int


class AbstractMessage(ABC):
    """
    Ant+ message
    """
    encoding_format: str
    message_id: int

    @classmethod
    @abstractmethod
    def _from_message(cls: Type[T], message: MessageData) -> T:
        """
        Creates an instance of the class by setting the values from the provided message
        This class method should not be called directly, only through the class method 'from_bytes'
        which adds validation of the checksum.
        """
        pass

    @classmethod
    def from_bytes(cls: Type[T], data: bytes) -> T:
        """
        Using the class field encoding_format, this method will unpack the provided bytes
        into a Tuple of ints.

        The contents of the message are used to calculate a checksum, which is then compared to
        the provided checksum to validate the message. If the message is valid, an instance of the class
        will be returned. If not, a ValueError is raised.
        """
        values = struct.unpack(cls.encoding_format, data)

        sync_byte = values[0]
        message_length = values[1]
        message_id = values[2]
        content = values[3:-1]
        checksum = values[-1]

        message = [sync_byte, message_length, message_id, *content]

        if not message_id == cls.message_id:
            raise ValueError(
                f'message id did not match for message {cls.__name__}, got {message} expected {cls.message_id}')

        if not checksum == calculate_checksum(message):
            raise ValueError(f'checksum did not match for message {cls.__name__}')

        message_data = MessageData(sync_byte, message_length, message_id, content, checksum)

        return cls._from_message(message_data)
