MESSAGE_SYNC = 0xA4  # 10100100 (most significant byte, msg)
MESSAGE_SYNC_LSB = 0xA5  # 10100101 (least significant byte, lsb)

# Configuration message ids
MESSAGE_UNASSIGN_CHANNEL = 0x41
MESSAGE_ASSIGN_CHANNEL = 0x42
MESSAGE_CHANNEL_ID = 0x51
MESSAGE_CHANNEL_PERIOD = 0x43
MESSAGE_CHANNEL_SEARCH_TIMEOUT = 0x44
MESSAGE_CHANNEL_RF_FREQUENCY = 0x45
MESSAGE_SET_NETWORK_KEY = 0x46
MESSAGE_TRANSMIT_POWER = 0x47
MESSAGE_SEARCH_WAVEFORM = 0x49
MESSAGE_ADD_CHANNEL_ID_TO_LIST = 0x59
MESSAGE_ADD_ENCRYPTION_ID_TO_LIST = 0x59
MESSAGE_CONFIG_ID_LIST = 0x5A
MESSAGE_CONFIG_ENCRYPTION_ID_LIST = 0x5A
MESSAGE_SET_CHANNEL_TRANSMIT_POWER = 0x60
MESSAGE_LOW_PRIORITY_SEARCH_TIMEOUT = 0x63
MESSAGE_SERIAL_NUMBER_SET_CHANNEL_ID = 0x65
MESSAGE_ENABLE_EXT_RX_MESSAGES = 0x66
MESSAGE_ENABLE_LED = 0x68
MESSAGE_ENABLE_CRYSTAL = 0x6D
MESSAGE_LIB_CONFIG = 0x6E
MESSAGE_FREQUENCY_AGILITY = 0x70
MESSAGE_PROXIMITY_SEARCH = 0x71
MESSAGE_CONFIGURE_EVENT_BUFFER = 0x74
MESSAGE_CHANNEL_SEARCH_PRIORITY = 0x75
MESSAGE_SET_128BIT_NETWORK_KEY = 0x76
MESSAGE_HIGH_DUTY_SEARCH = 0x77
MESSAGE_CONFIGURE_ADVANCED_BURST = 0x78
MESSAGE_CONFIGURE_EVENT_FILTER = 0x79
MESSAGE_CONFIGURE_SELECTIVE_DATA_UPDATES = 0x7A
MESSAGE_SET_SELECTIVE_DATA_UPDATE_MASK = 0x7B
MESSAGE_CONFIGURE_USER_NVM = 0x7C
MESSAGE_ENABLE_SINGLE_CHANNEL_ENCRYPTION = 0x7D
MESSAGE_SET_ENCRYPTION_KEY = 0x7E
MESSAGE_SET_ENCRYPTION_INFO = 0x7F
MESSAGE_CHANNEL_SEARCH_SHARING = 0x81
MESSAGE_LOAD_STORE_ENCRYPTION_KEY = 0x83
MESSAGE_SET_USB_DESCRIPTOR_STRING = 0xC7

# Notification message ids
MESSAGE_START_UP_MESSAGE = 0x6F
MESSAGE_SERIAL_ERROR_MESSAGE = 0xAE

# Control message ids
MESSAGE_RESET_SYSTEM = 0x4A
MESSAGE_OPEN_CHANNEL = 0x4B
MESSAGE_CLOSE_CHANNEL = 0x4C
MESSAGE_REQUEST_MESSAGE = 0x4D
MESSAGE_OPEN_RX_SCAN_MODE = 0x5B
MESSAGE_SLEEP_MESSAGE = 0xC5

# Data message ids
MESSAGE_BROADCAST_DATA = 0x4E
MESSAGE_ACKNOWLEDGED_DATA = 0x4F
MESSAGE_BURST_TRANSFER_DATA = 0x50
MESSAGE_ADVANCED_BURST_DATA = 0x72

# Channel message ids
MESSAGE_CHANNEL_EVENT = 0x40
MESSAGE_CHANNEL_RESPONSE = 0x40

# Requested response message ids
MESSAGE_CHANNEL_STATUS = 0x52
MESSAGE_ANT_VERSION = 0x3E
MESSAGE_CAPABILITIES = 0x54
MESSAGE_SERIAL_NUMBER = 0x61
MESSAGE_EVENT_BUFFER_CONFIGURATION = 0x74
MESSAGE_ADVANCED_BURST_CAPABILITIES = 0x78
MESSAGE_ADVANCED_BURST_CURRENT_CONFIGURATION = 0x78
MESSAGE_EVENT_FILTER = 0x79
MESSAGE_SELECTIVE_DATA_UPDATE_MASK_SETTINGS = 0x7B
MESSAGE_USER_NVM = 0x7C
MESSAGE_ENCRYPTION_MODE_PARAMETERS = 0x7D

# Test mode message ids
MESSAGE_CW_INIT = 0x53
MESSAGE_CW_TEST = 0x48

# Extended data message ids (legacy)
MESSAGE_EXTENDED_BROADCAST_DATA = 0x5D
MESSAGE_EXTENDED_ACKNOWLEDGED_DATA = 0x5E
MESSAGE_EXTENDED_BURST_DATA = 0x5F

# Channel response constants
RESPONSE_NO_ERROR = 0x00
EVENT_RX_SEARCH_TIMEOUT = 0x01
EVENT_RX_FAIL = 0x02
EVENT_TX = 0x03
EVENT_TRANSFER_RX_FAILED = 0x04
EVENT_TRANSFER_TX_COMPLETED = 0x05
EVENT_TRANSFER_TX_FAILED = 0x06
EVENT_CHANNEL_CLOSED = 0x07
EVENT_RX_FAIL_GO_TO_SEARCH = 0x08
EVENT_CHANNEL_COLLISION = 0x09
EVENT_TRANSFER_TX_START = 0x0A
EVENT_TRANSFER_NEXT_DATA_BLOCK = 0x11
CHANNEL_IN_WRONG_STATE = 0x15
CHANNEL_NOT_OPENED = 0x16
CHANNEL_ID_NOT_SET = 0x18
CLOSE_ALL_CHANNELS = 0x19
TRANSFER_IN_PROGRESS = 0x1F
TRANSFER_SEQUENCE_NUMBER_ERROR = 0x20
TRANSFER_IN_ERROR = 0x21
# TRANSFER_BUSY = ? missing from doc
MESSAGE_SIZE_EXCEEDS_LIMIT = 0x27
INVALID_MESSAGE = 0x28
INVALID_NETWORK_NUMBER = 0x29
INVALID_LIST_ID = 0x30
INVALID_SCAN_TX_CHANNEL = 0x31
INVALID_PARAMETER_PROVIDED = 0x33
EVENT_SERIAL_QUE_OVERFLOW = 0x34
EVENT_QUE_OVERFLOW = 0x35
NVM_FULL_ERROR = 0x40
NVM_WRITE_ERROR = 0x41
USB_STRING_WRITE_FAIL = 0x70
MESG_SERIAL_ERROR_ID = 0xAE
ENCRYPT_NEGOTIATION_SUCCESS = 0x38
ENCRYPT_NEGOTIATION_FAIL = 0x39

EVENT_LABELS = {
    RESPONSE_NO_ERROR: "RESPONSE_NO_ERROR",
    EVENT_RX_SEARCH_TIMEOUT: "EVENT_RX_SEARCH_TIMEOUT",
    EVENT_RX_FAIL: "EVENT_RX_FAIL",
    EVENT_TX: "EVENT_TX",
    EVENT_TRANSFER_RX_FAILED: "EVENT_TRANSFER_RX_FAILED",
    EVENT_TRANSFER_TX_COMPLETED: "EVENT_TRANSFER_TX_COMPLETED",
    EVENT_TRANSFER_TX_FAILED: "EVENT_TRANSFER_TX_FAILED",
    EVENT_CHANNEL_CLOSED: "EVENT_CHANNEL_CLOSED",
    EVENT_RX_FAIL_GO_TO_SEARCH: "EVENT_RX_FAIL_GO_TO_SEARCH",
    EVENT_CHANNEL_COLLISION: "EVENT_CHANNEL_COLLISION",
    EVENT_TRANSFER_TX_START: "EVENT_TRANSFER_TX_START",
    EVENT_TRANSFER_NEXT_DATA_BLOCK: "EVENT_TRANSFER_NEXT_DATA_BLOCK",
    CHANNEL_IN_WRONG_STATE: "CHANNEL_IN_WRONG_STATE",
    CHANNEL_NOT_OPENED: "CHANNEL_NOT_OPENED",
    CHANNEL_ID_NOT_SET: "CHANNEL_ID_NOT_SET",
    CLOSE_ALL_CHANNELS: "CLOSE_ALL_CHANNELS",
    TRANSFER_IN_PROGRESS: "TRANSFER_IN_PROGRESS",
    TRANSFER_SEQUENCE_NUMBER_ERROR: "TRANSFER_SEQUENCE_NUMBER_ERROR",
    TRANSFER_IN_ERROR: "TRANSFER_IN_ERROR",
    MESSAGE_SIZE_EXCEEDS_LIMIT: "MESSAGE_SIZE_EXCEEDS_LIMIT",
    INVALID_MESSAGE: "INVALID_MESSAGE",
    INVALID_NETWORK_NUMBER: "INVALID_NETWORK_NUMBER",
    INVALID_LIST_ID: "INVALID_LIST_ID",
    INVALID_SCAN_TX_CHANNEL: "INVALID_SCAN_TX_CHANNEL",
    INVALID_PARAMETER_PROVIDED: "INVALID_PARAMETER_PROVIDED",
    EVENT_SERIAL_QUE_OVERFLOW: "EVENT_SERIAL_QUE_OVERFLOW",
    EVENT_QUE_OVERFLOW: "EVENT_QUE_OVERFLOW",
    NVM_FULL_ERROR: "NVM_FULL_ERROR",
    NVM_WRITE_ERROR: "NVM_WRITE_ERROR",
    USB_STRING_WRITE_FAIL: "USB_STRING_WRITE_FAIL",
    MESG_SERIAL_ERROR_ID: "MESG_SERIAL_ERROR_ID",
    ENCRYPT_NEGOTIATION_SUCCESS: "ENCRYPT_NEGOTIATION_SUCCESS",
    ENCRYPT_NEGOTIATION_FAIL: "ENCRYPT_NEGOTIATION_FAIL",
}
