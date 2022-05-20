# This code is part of OpenFE and is licensed under the MIT license.
# For details, see https://github.com/OpenFreeEnergy/gufe

"""The `ProtocolUnit` class should be subclassed for all units to be used as
part of a `ProtocolDAG`.

"""

import abc
from os import PathLike
from typing import Iterable, List, Dict, Any

from .results import ProtocolUnitResult


class ProtocolUnit(abc.ABC):
    """A unit of work computable by

    """

    def __init__(
            self,
            settings: "ProtocolSettings", # type: ignore
            **kwargs
        ):

        self._settings = settings
        self._kwargs = kwargs

    def __hash__(self):
        ...

    @property
    def settings(self):
        return self._settings

    def execute(self, dependency_results, block=True) -> ProtocolUnitResult:
        """Given `ProtocolUnitResult`s from dependencies, execute this `ProtocolUnit`.

        Parameters
        ----------
        block : bool
            If `True`, block until execution completes; otherwise run in its own thread.

        """
        if block:
            out = self._execute(dependency_results)
            result = ProtocolUnitResult(
                                name=self.__class__.__name__,
                                dependencies=dependency_results, 
                                **out)

        else:
            #TODO: wrap in a thread; update status
            ...

        return result


    @abc.abstractmethod
    def _execute(self, dependency_results: List[ProtocolUnitResult]) -> Dict[str, Any]:
        ...

    @property
    def result(self) -> ProtocolUnitResult:
        """Return `ProtocolUnitResult` for this `ProtocolUnit`.

        Requires `status` == "COMPLETE"; exception raised otherwise.

        """
        return self._result

    def get_artifacts(self) -> Dict[str, PathLike]:
        """Return a dict of file-like artifacts produced by this
        `ProtocolUnit`.

        """
        ...
