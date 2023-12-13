from __future__ import annotations
from typing import TYPE_CHECKING
import math
import smoothmath as sm
import smoothmath.expression as ex
import smoothmath._private.expression.base as base
if TYPE_CHECKING:
    from smoothmath._private.local_differential import LocalDifferentialBuilder
    from smoothmath._private.global_differential import GlobalDifferentialBuilder


class Power(base.BinaryExpression):
    def __init__(
        self: Power,
        left: sm.Expression,
        right: sm.Expression
    ) -> None:
        super().__init__(left, right)

    def _verify_domain_constraints(
        self: Power,
        left_value: sm.real_number,
        right_value: sm.real_number
    ) -> None:
        if left_value == 0:
            if right_value > 0:
                raise sm.DomainError("Power(x, y) is not smooth around x = 0 for y > 0")
            elif right_value == 0:
                raise sm.DomainError("Power(x, y) is not smooth around (x = 0, y = 0)")
            else: # right_value < 0
                raise sm.DomainError("Power(x, y) blows up around x = 0 for y < 0")
        elif left_value < 0:
            raise sm.DomainError("Power(x, y) is undefined for x < 0")

    def _value_formula(
        self: Power,
        left_value: sm.real_number,
        right_value: sm.real_number
    ) -> sm.real_number:
        return left_value ** right_value

    def _local_partial(
        self: Power,
        point: sm.Point,
        with_respect_to: str
    ) -> sm.real_number:
        if self._left._lacks_variables and self._left._evaluate(point) == 1:
            # If we find something like `Constant(1) ** Whatever`, we can short-circuit.
            return 0
        else:
            left_value = self._left._evaluate(point)
            right_value = self._right._evaluate(point)
            self._verify_domain_constraints(left_value, right_value)
            left_partial = self._left._local_partial(point, with_respect_to)
            right_partial = self._right._local_partial(point, with_respect_to)
            return (
                self._local_partial_formula_left(point, left_partial) +
                self._local_partial_formula_right(point, right_partial)
            )

    def _synthetic_partial(
        self: Power,
        with_respect_to: str
    ) -> sm.Expression:
        left_partial = self._left._synthetic_partial(with_respect_to)
        right_partial = self._right._synthetic_partial(with_respect_to)
        return ex.Plus(
            self._synthetic_partial_formula_left(left_partial),
            self._synthetic_partial_formula_right(right_partial)
        )

    def _compute_local_differential(
        self: Power,
        builder: LocalDifferentialBuilder,
        accumulated: sm.real_number
    ) -> None:
        if self._left._lacks_variables and self._left._evaluate(builder.point) == 1:
            # If we find something like `Constant(1) ** Whatever`, we can short-circuit.
            pass
        else:
            left_value = self._left._evaluate(builder.point)
            right_value = self._right._evaluate(builder.point)
            self._verify_domain_constraints(left_value, right_value)
            next_accumulated_left = self._local_partial_formula_left(builder.point, accumulated)
            next_accumulated_right = self._local_partial_formula_right(builder.point, accumulated)
            self._left._compute_local_differential(builder, next_accumulated_left)
            self._right._compute_local_differential(builder, next_accumulated_right)

    def _compute_global_differential(
        self: Power,
        builder: GlobalDifferentialBuilder,
        accumulated: sm.Expression
    ) -> None:
        next_accumulated_left = self._synthetic_partial_formula_left(accumulated)
        next_accumulated_right = self._synthetic_partial_formula_right(accumulated)
        self._left._compute_global_differential(builder, next_accumulated_left)
        self._right._compute_global_differential(builder, next_accumulated_right)

    def _local_partial_formula_left(
        self: Power,
        point: sm.Point,
        multiplier: sm.real_number
    ) -> sm.real_number:
        left_value = self._left._evaluate(point)
        right_value = self._right._evaluate(point)
        return right_value * (left_value ** (right_value - 1)) * multiplier

    def _local_partial_formula_right(
        self: Power,
        point: sm.Point,
        multiplier: sm.real_number
    ) -> sm.real_number:
        left_value = self._left._evaluate(point)
        self_value = self._evaluate(point)
        return math.log(left_value) * self_value * multiplier

    def _synthetic_partial_formula_left(
        self: Power,
        multiplier: sm.Expression
    ) -> sm.Expression:
        return ex.Multiply(
            ex.Multiply(self._right, ex.Power(self._left, ex.Minus(self._right, ex.Constant(1)))),
            multiplier
        )

    def _synthetic_partial_formula_right(
        self: Power,
        multiplier: sm.Expression
    ) -> sm.Expression:
        return ex.Multiply(ex.Multiply(ex.Logarithm(self._left, base = math.e), self), multiplier)
