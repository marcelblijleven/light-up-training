class ChannelResponseException(Exception):
    def __init__(self, message_code: int, event_label: str):
        message = f'channel response message received with message code {message_code} ({event_label})'
        super().__init__(message)
