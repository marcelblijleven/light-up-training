from contextlib import contextmanager

import pytest

from lightuptraining.sources.antplus.messages.util import calculate_checksum, validate_device_number, \
    device_number_to_fields, fields_to_device_number, set_pairing_bit_on_device_type, split_pairing_bit_from_device_type


@contextmanager
def does_not_raise():
    yield


@pytest.mark.parametrize(['message', 'expected'], [
    ([164, 1, 65, 1], 229),
    ([164, 4, 65, 1, 255, 128, 30], 129),
    ([164, 5, 81, 1, 232, 3, 248, 10], 232),
    ([164, 3, 67, 1, 134, 31], 124),
])
def test_calculate_checksum(message, expected):
    assert expected == calculate_checksum(message)


@pytest.mark.parametrize(['number', 'expectation'], [
    (0, does_not_raise()),
    (65535, does_not_raise()),
    (32765, does_not_raise()),
    (-1, pytest.raises(ValueError)),
    (65536, pytest.raises(ValueError)),
])
def test_validate_device_number(number, expectation):
    with expectation:
        validate_device_number(number)


@pytest.mark.parametrize(['number', 'expected'], [
    (1000, [232, 3]),
    (0, [0, 0]),
    (65535, [255, 255]),
])
def test_device_number_to_fields(number, expected):
    assert expected == device_number_to_fields(number)


@pytest.mark.parametrize(['fields', 'expected'], [
    ([232, 3], 1000),
    ([0, 0], 0),
    ([255, 255], 65535),
])
def test_fields_to_device_number(fields, expected):
    assert expected == fields_to_device_number(fields)


@pytest.mark.parametrize(['pairing_bit', 'device_type', 'expected'], [
    (0, 11, 11),
    (0, 16, 16),
    (0, 17, 17),
    (0, 18, 18),
    (0, 19, 19),
    (0, 25, 25),
    (0, 119, 119),
    (0, 120, 120),
    (0, 121, 121),
    (0, 122, 122),
    (0, 123, 123),
    (0, 124, 124),
    (0, 1, 1),
    (1, 11, 139),
    (1, 16, 144),
    (1, 17, 145),
    (1, 18, 146),
    (1, 19, 147),
    (1, 25, 153),
    (1, 119, 247),
    (1, 120, 248),
    (1, 121, 249),
    (1, 122, 250),
    (1, 123, 251),
    (1, 124, 252),
    (1, 1, 129),
])
def test_set_pairing_bit_on_device_type(pairing_bit, device_type, expected):
    assert expected == set_pairing_bit_on_device_type(pairing_bit, device_type)


@pytest.mark.parametrize(['device_type_with_pairing_bit', 'expected'], [
    (11, (0, 11)),
    (16, (0, 16)),
    (17, (0, 17)),
    (18, (0, 18)),
    (19, (0, 19)),
    (25, (0, 25)),
    (119, (0, 119)),
    (120, (0, 120)),
    (121, (0, 121)),
    (122, (0, 122)),
    (123, (0, 123)),
    (124, (0, 124)),
    (1, (0, 1)),
    (139, (1, 11)),
    (144, (1, 16)),
    (145, (1, 17)),
    (146, (1, 18)),
    (147, (1, 19)),
    (153, (1, 25)),
    (247, (1, 119)),
    (248, (1, 120)),
    (249, (1, 121)),
    (250, (1, 122)),
    (251, (1, 123)),
    (252, (1, 124)),
    (129, (1, 1)),
])
def test_split_pairing_bit_from_device_type(device_type_with_pairing_bit, expected):
    assert expected == split_pairing_bit_from_device_type(device_type_with_pairing_bit)
