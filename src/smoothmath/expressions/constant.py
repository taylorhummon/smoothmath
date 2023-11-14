from __future__ import annotations
from typing import Any, TYPE_CHECKING
if TYPE_CHECKING:
    from smoothmath.typing import real_number
    from smoothmath.all_partials import AllPartials
    from smoothmath.variable_values import VariableValues

# imports needed for class declaration
from smoothmath.expressions.nullary_expression import NullaryExpression

class Constant(NullaryExpression):
    def __init__(
        self: Constant,
        value: real_number
    ) -> None:
        super().__init__(lacks_variables = True)
        self._value: real_number
        self._value = value

    def _evaluate(
        self: Constant,
        variable_values: VariableValues
    ) -> real_number:
        return self._value

    def _partial_at(
        self: Constant,
        variable_values: VariableValues,
        with_respect_to: str
    ) -> real_number:
        return 0

    def _compute_all_partials_at(
        self: Constant,
        all_partials: AllPartials,
        variable_values: VariableValues,
        seed: real_number
    ) -> None:
        pass

    def __eq__(
        self: Constant,
        other: Any
    ) -> bool:
        return isinstance(other, Constant) and (other._value == self._value)

    def __str__(
        self: Constant
    ) -> str:
        return str(self._value)
