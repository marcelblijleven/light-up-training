from abc import ABC
from typing import List, Tuple, Protocol


class Profile(Protocol):
    channel_type: int
    network_key: List[int]
    rf_channel_frequency: int
    channel_id: Tuple[int, int, int]
    channel_period: int
    search_timeout: int


class AbstractProfile(ABC):
    channel_type: int
    network_key: List[int]
    rf_channel_frequency: int
    channel_id: Tuple[int, int, int]
    channel_period: int
    search_timeout: int

    def _set_channel_id(self, device_type: int, device_number: int, transmission_type: int):
        """
        Sets the channel id (device type, device number, transmission type)
        """
        self.channel_id = (device_type, device_number, transmission_type)
