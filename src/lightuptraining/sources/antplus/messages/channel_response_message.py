from typing import Type

from lightuptraining.sources.antplus.messages import const
from lightuptraining.sources.antplus.messages.exceptions import ChannelResponseException
from lightuptraining.sources.antplus.messages.message import AbstractMessage, MessageData, T


class ChannelResponseMessage(AbstractMessage):
    message_id = 0x40
    encoding_format = '<BBBBBBB'

    def __init__(self, response_channel_id: int, response_message_id: int, response_message_code: int):
        self.response_channel_id = response_channel_id
        self.response_message_id = response_message_id
        self.response_message_code = response_message_code

    @property
    def response_no_error(self) -> bool:
        """
        Checks if the response message code equals RESPONSE_NO_ERROR (0x00)
        """
        return self.response_message_code == const.RESPONSE_NO_ERROR

    def get_event_label(self) -> str:
        """
        Returns the human readable event label for the received message code
        """
        return const.EVENT_LABELS[self.response_message_code]

    def raise_for_message_code(self):
        """
        Raises a ChannelResponseException when response message code does not equal
        RESPONSE_NO_ERROR (0x00)
        """
        if not self.response_no_error:
            raise ChannelResponseException(message_code=self.response_message_code, event_label=self.get_event_label())

    @classmethod
    def _from_message(cls: Type[T], message: MessageData) -> T:
        content = message.content
        response_channel_id = content[0]
        response_message_id = content[1]
        response_message_code = content[2]
        return cls(response_channel_id, response_message_id, response_message_code)
