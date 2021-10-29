import struct
from functools import reduce
from operator import ixor
from typing import Iterable, List, Tuple, Union


def calculate_checksum(message: Iterable[int]) -> int:
    """
    Calculates the checksum, which is the XOR of all bytes in the message
    """
    return reduce(ixor, message)


def validate_device_number(device_number: int):
    """
    Validates the device number and raises a ValueError when the device number is out of range
    Device number is a 16 bit field, so the value must be between 0x0000 and 0xFFFF (0 and 65535)
    """
    if not 0x0000 <= device_number <= 0xFFFF:
        raise ValueError('device number out of range (0x0000 <= device_number <= 0xFFFF)')


def device_number_to_fields(device_number: int) -> List[int]:
    """
    Splits the device number (16 bits) into two bytes

    Example with device number 1000
    Full bits:      0b0000001111101000
    First 8 bits:   0b00000011 == 3
    Last 8 bits:    0b11101000 == 232

    This function will return [232, 3] because the byte order is little endian (least significant byte first)
    """
    return [byte for byte in struct.pack('<H', device_number)]


def fields_to_device_number(fields: Union[Tuple[int], List[int]]) -> int:
    """
    Joins the two 8 bit fields into a 16 bit device number

    Example with fields 3 and 232
    3:      0b00000011
    232:    0b11101000
    1000:   (3 << 8) | 232
            (3 << 8) == 0b1100000000
            0b1100000000 | 232 == 1000
    """
    # return struct.unpack('<H', bytes(fields))[0]
    return (fields[1] << 8) | fields[0]


def validate_device_type(device_type: int):
    """
    Validates the device type, the device type is sent to the ant+ device together with a pairing bit.
    The most significant bit is the pairing bit

    Max value of the pairing bit with device type is 255
    Because True << 7 equals 128, the max value of device type is 255 - 128 == 127
    """
    if not 0 <= device_type <= 127:
        raise ValueError('device type out of range (0 <= device_type <= 127)')


def set_pairing_bit_on_device_type(pairing_bit: bool, device_type: int):
    """
    Shifts the pairing bit (True = 1, False = 0) 7 bits to the left and adds
    the device type
    """
    return (pairing_bit << 7) + device_type


def split_pairing_bit_from_device_type(device_type_with_pairing_bit: int) -> Tuple[int, int]:
    """
    Splits the device type with pairing bit into the pairing bit and device type

    Converts the int to a binary string, padded to a length of 8 bits, to retrieve the pairing bit
    The left most bit is the pairing bit, the rest of the bits form the device type
    """
    if not 0 <= device_type_with_pairing_bit <= 255:
        raise ValueError('device type with pairing bit out of range (0 <= x <= 255)')

    binary_string = format(device_type_with_pairing_bit, '08b')
    pairing_bit = int(binary_string[0])
    device_type = (pairing_bit << 7) ^ device_type_with_pairing_bit
    return pairing_bit, device_type
