from typing import List

from lightuptraining.sources.antplus.profiles.const import SLAVE_RECEIVE_ONLY_CHANNEL, DEFAULT_SEARCH_TIMEOUT, \
    DEVICE_TYPE_HEART_RATE
from lightuptraining.sources.antplus.profiles.profile import AbstractProfile


class HeartRateMonitorProfile(AbstractProfile):
    channel_type = SLAVE_RECEIVE_ONLY_CHANNEL  # BIDIRECTIONAL_SLAVE_CHANNEL
    rf_channel_frequency = 0x39  # 57
    channel_period = 8070
    search_timeout = DEFAULT_SEARCH_TIMEOUT

    def __init__(self, network_key: List[int], device_number: int = 0, transmission_type: int = 0):
        """
        Device number and transmission type have default value of 0, which acts as a wildcard while searching
        for devices.
        """
        self._set_channel_id(DEVICE_TYPE_HEART_RATE, device_number, transmission_type)
        self.network_key = network_key
