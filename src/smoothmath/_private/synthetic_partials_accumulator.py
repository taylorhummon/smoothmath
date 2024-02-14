from __future__ import annotations
from typing import TYPE_CHECKING
import smoothmath._private.utilities as util
if TYPE_CHECKING:
    from smoothmath import Expression
    from smoothmath.expression import Variable


class SyntheticPartialsAccumulator:
    def __init__(
        self: SyntheticPartialsAccumulator
    ) -> None:
        self.synthetic_partials: dict[str, Expression]
        self.synthetic_partials = {}

    def add_to(
        self: SyntheticPartialsAccumulator,
        variable: Variable | str,
        contribution: Expression
    ) -> None:
        variable_name = util.get_variable_name(variable)
        existing = self.synthetic_partials.get(variable_name, None)
        next = existing + contribution if existing is not None else contribution
        self.synthetic_partials[variable_name] = next
