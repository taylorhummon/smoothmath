from __future__ import annotations
from typing import TYPE_CHECKING
import smoothmath._private.expression.variable as va
if TYPE_CHECKING:
    from smoothmath import RealNumber, Expression
    from smoothmath.expression import Variable


class NumericPartialsAccumulator:
    def __init__(
        self: NumericPartialsAccumulator
    ) -> None:
        self.numeric_partials: dict[str, RealNumber]
        self.numeric_partials = {}

    def add_to(
        self: NumericPartialsAccumulator,
        variable: Variable | str,
        contribution: RealNumber
    ) -> None:
        variable_name = va.get_variable_name(variable)
        existing = self.numeric_partials.get(variable_name, 0)
        self.numeric_partials[variable_name] = existing + contribution


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
        variable_name = va.get_variable_name(variable)
        existing = self.synthetic_partials.get(variable_name, None)
        next = existing + contribution if existing is not None else contribution
        self.synthetic_partials[variable_name] = next
