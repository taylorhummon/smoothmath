from __future__ import annotations
from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:
    from smoothmath.types import real_number
    from smoothmath.variable_values import VariableValues
    from smoothmath.all_partials import AllPartials
    from smoothmath.synthetic import Synthetic
    from smoothmath.expression import Expression

from smoothmath.expression import NullaryExpression
import smoothmath.expressions as ex


# differential rule: d(C) = 0

class Constant(NullaryExpression):
    def __init__(
        self: Constant,
        value: real_number
    ) -> None:
        super().__init__(lacks_variables = True)
        self._value: real_number
        self._value = value

    def __eq__(
        self: Constant,
        other: Any
    ) -> bool:
        return isinstance(other, Constant) and (other._value == self._value)

    def __hash__(
        self: Constant
    ) -> int:
        if self._cached_hash is None:
            self._cached_hash = hash(self._value)
        return self._cached_hash

    def __str__(
        self: Constant
    ) -> str:
        return f"Constant({self._value})"

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
        accumulated: real_number
    ) -> None:
        pass

    def _synthetic_partial(
        self: Constant,
        with_respect_to: str
    ) -> Expression:
        return ex.Constant(0)

    def _compute_all_synthetic_partials(
        self: Constant,
        synthetic: Synthetic,
        accumulated: Expression
    ) -> None:
        pass
