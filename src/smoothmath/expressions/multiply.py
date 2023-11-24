from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from smoothmath.types import real_number
    from smoothmath.variable_values import VariableValues
    from smoothmath.all_partials import AllPartials
    from smoothmath.synthetic import Synthetic
    from smoothmath.expression import Expression

from smoothmath.expression import BinaryExpression
from smoothmath.errors import DomainError
import smoothmath.expressions as ex


# differential rule: d(a * b) = b * da + a * db

class Multiply(BinaryExpression):
    def __init__(
        self: Multiply,
        a: Expression,
        b: Expression
    ) -> None:
        super().__init__(a, b)

    def _evaluate(
        self: Multiply,
        variable_values: VariableValues
    ) -> real_number:
        pair_or_none = self._get_a_and_b_values_or_none(variable_values)
        if pair_or_none == None:
            self._value = 0
        else: # pair_or_none is the pair (a_value, b_value)
            a_value, b_value = pair_or_none
            self._value = a_value * b_value
        return self._value

    def _partial_at(
        self: Multiply,
        variable_values: VariableValues,
        with_respect_to: str
    ) -> real_number:
        pair_or_none = self._get_a_and_b_values_or_none(variable_values)
        if pair_or_none == None:
            return 0
        else: # pair_or_none is the pair (a_value, b_value)
            a_value, b_value = pair_or_none
            a_partial = self._a._partial_at(variable_values, with_respect_to)
            b_partial = self._b._partial_at(variable_values, with_respect_to)
            return b_value * a_partial + a_value * b_partial

    def _compute_all_partials_at(
        self: Multiply,
        all_partials: AllPartials,
        variable_values: VariableValues,
        accumulated: real_number
    ) -> None:
        pair_or_none = self._get_a_and_b_values_or_none(variable_values)
        if pair_or_none == None:
            return
        else: # pair_or_none is the pair (a_value, b_value)
            a_value, b_value = pair_or_none
            self._a._compute_all_partials_at(all_partials, variable_values, accumulated * b_value)
            self._b._compute_all_partials_at(all_partials, variable_values, accumulated * a_value)

    def _synthetic_partial(
        self: Multiply,
        with_respect_to: str
    ) -> Expression:
        a_partial = self._a._synthetic_partial(with_respect_to)
        b_partial = self._b._synthetic_partial(with_respect_to)
        return ex.Plus(
            ex.Multiply(self._b, a_partial),
            ex.Multiply(self._a, b_partial)
        )

    def _compute_all_synthetic_partials(
        self: Multiply,
        synthetic: Synthetic,
        accumulated: Expression
    ) -> None:
        self._a._compute_all_synthetic_partials(synthetic, ex.Multiply(accumulated, self._b))
        self._b._compute_all_synthetic_partials(synthetic, ex.Multiply(accumulated, self._a))

    # the following method is used to allow shirt-circuiting of either a * 0 or 0 * b
    def _get_a_and_b_values_or_none(
        self: Multiply,
        variable_values: VariableValues
    ) -> tuple[real_number, real_number] | None:
        try:
            a_value = self._a._evaluate(variable_values)
        except DomainError as error:
            try:
                b_value_inner = self._b._evaluate(variable_values)
            except DomainError:
                raise error
            if b_value_inner == 0:
                return None
            raise
        try:
            b_value = self._b._evaluate(variable_values)
        except DomainError as error:
            try:
                a_value_inner = self._a._evaluate(variable_values)
            except DomainError:
                raise error
            if a_value_inner == 0:
                return None
            raise
        return (a_value, b_value)
