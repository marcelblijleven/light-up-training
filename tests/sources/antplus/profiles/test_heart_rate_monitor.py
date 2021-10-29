from lightuptraining.sources.antplus.profiles.const import DEVICE_TYPE_HEART_RATE, SLAVE_RECEIVE_ONLY_CHANNEL, \
    DEFAULT_SEARCH_TIMEOUT
from lightuptraining.sources.antplus.profiles.heart_rate_monitor import HeartRateMonitorProfile


def test_heart_rate_monitor():
    network_key = [1, 2, 3, 4, 5, 6, 7, 8]
    device_number = 10000
    transmission_type = 1
    hrm = HeartRateMonitorProfile(network_key, device_number, transmission_type)

    assert hrm.network_key == network_key
    assert hrm.channel_id == (DEVICE_TYPE_HEART_RATE, device_number, transmission_type)
    assert hrm.channel_type == SLAVE_RECEIVE_ONLY_CHANNEL
    assert hrm.channel_period == 8070
    assert hrm.rf_channel_frequency == 0x39
    assert hrm.search_timeout == DEFAULT_SEARCH_TIMEOUT


def test_heart_rate_monitor_wildcards():
    network_key = [1, 2, 3, 4, 5, 6, 7, 8]
    hrm = HeartRateMonitorProfile(network_key)

    assert hrm.channel_id == (DEVICE_TYPE_HEART_RATE, 0, 0)
