class USBDeviceException(Exception):
    """
    Raised when an USB exception occurred
    """
    def __init__(self, message: str, vendor_id: int, product_id: int):
        message = f'{message} (usb device vendor id {vendor_id} product id {product_id})'
        super().__init__(message)
