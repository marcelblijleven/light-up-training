from abc import ABC
from typing import List, Dict

from lightuptraining.protocols import SupportsNotify


class Source(ABC):
    _outputs: List[SupportsNotify] = []

    def _notify(self, data: Dict[str, int]):
        """
        Updates all outputs with provided data
        """
        for output in self._outputs:
            output.notify(data)

    def start(self):
        """
        Starts the source
        """
        raise NotImplementedError

    def stop(self):
        """
        Stops the source
        """
        raise NotImplementedError

    def attach_output(self, output: SupportsNotify):
        """
        Attaches the output to the source, whenever data is returned from the source, all attached outputs
        will be updated with the value of the incoming data.
        """
        raise NotImplementedError

    def remove_output(self, output: SupportsNotify):
        """
        Removes output from the source
        """
        raise NotImplementedError
