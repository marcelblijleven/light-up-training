from abc import abstractmethod
from typing import Protocol, runtime_checkable

import usb


@runtime_checkable
class Device(Protocol):

    @property
    @abstractmethod
    def endpoint_in(self) -> usb.core.Endpoint:
        pass

    @property
    @abstractmethod
    def is_open(self) -> bool:
        pass

    def close(self) -> None:
        pass
