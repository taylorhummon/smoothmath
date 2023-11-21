from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from smoothmath.types import real_number
    from smoothmath.variable_values import VariableValues
    from smoothmath.all_partials import AllPartials
    from smoothmath.expression import Expression

from smoothmath.expression import BinaryExpression
from smoothmath.errors import DomainError
import smoothmath.expressions as ex


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
        pairOrNone = self._get_a_and_b_values_or_none(variable_values)
        if pairOrNone == None:
            self._value = 0
        else: # pairOrNone is the pair (a_value, b_value)
            a_value, b_value = pairOrNone
            self._value = a_value * b_value
        return self._value

    def _partial_at(
        self: Multiply,
        variable_values: VariableValues,
        with_respect_to: str
    ) -> real_number:
        pairOrNone = self._get_a_and_b_values_or_none(variable_values)
        if pairOrNone == None:
            return 0
        else: # pairOrNone is the pair (a_value, b_value)
            a_value, b_value = pairOrNone
            a_partial = self._a._partial_at(variable_values, with_respect_to)
            b_partial = self._b._partial_at(variable_values, with_respect_to)
            # d(a * b) = b * da + a * db
            return b_value * a_partial + a_value * b_partial

    def _compute_all_partials_at(
        self: Multiply,
        all_partials: AllPartials,
        variable_values: VariableValues,
        seed: real_number
    ) -> None:
        pairOrNone = self._get_a_and_b_values_or_none(variable_values)
        if pairOrNone == None:
            return
        else: # pairOrNone is the pair (a_value, b_value)
            a_value, b_value = pairOrNone
            # d(a * b) = b * da + a * db
            self._a._compute_all_partials_at(all_partials, variable_values, seed * b_value)
            self._b._compute_all_partials_at(all_partials, variable_values, seed * a_value)

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
