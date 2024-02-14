from __future__ import annotations
from typing import TYPE_CHECKING
import smoothmath._private.utilities as util
if TYPE_CHECKING:
    from smoothmath import RealNumber, Point
    from smoothmath.expression import Variable


class LocalPartialsAccumulator:
    def __init__(
        self: LocalPartialsAccumulator,
        point: Point
    ) -> None:
        self.point: Point
        self.point = point
        self.local_partials: dict[str, RealNumber]
        self.local_partials = {}

    def add_to(
        self: LocalPartialsAccumulator,
        variable: Variable | str,
        contribution: RealNumber
    ) -> None:
        variable_name = util.get_variable_name(variable)
        existing = self.local_partials.get(variable_name, 0)
        self.local_partials[variable_name] = existing + contribution
