from typing import Protocol, runtime_checkable


@runtime_checkable
class SupportsNotify(Protocol):
    """
    Has a notify method which takes a Dict[str, int] value argument.
    """
    def notify(self, value: dict[str, int]) -> None:
        pass


@runtime_checkable
class IsSource(Protocol):
    """
    Implements a start, stop, attach_output and remove_output method.

    The attach_output and remove_output method take a single argument
    which must implement the SupportsNotify protocol
    """
    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass

    def attach_output(self, output: SupportsNotify) -> None:
        pass

    def remove_output(self, output: SupportsNotify) -> None:
        pass
