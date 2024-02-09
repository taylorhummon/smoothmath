from __future__ import annotations
from typing import TYPE_CHECKING, Callable, Optional
import smoothmath as sm
import smoothmath.expression as ex
import smoothmath._private.base_expression as base
from smoothmath._private.math_functions import negation, nth_power, divide, add, multiply
if TYPE_CHECKING:
    from smoothmath import RealNumber
    from smoothmath._private.local_differential import LocalDifferentialBuilder
    from smoothmath._private.global_differential import GlobalDifferentialBuilder


class Divide(base.BinaryExpression):
    """
    Division.

    :param left: the numerator
    :param right: the denominator
    """

    ## Evaluation ##

    def _verify_domain_constraints(
        self: Divide,
        left_value: RealNumber,
        right_value: RealNumber
    ) -> None:
        if right_value == 0:
            if left_value == 0:
                raise sm.DomainError("Divide(x, y) is not smooth around (x = 0, y = 0)")
            else: # left_value != 0
                raise sm.DomainError("Divide(x, y) blows up around x != 0 and y = 0")

    def _value_formula(
        self: Divide,
        left_value: RealNumber,
        right_value: RealNumber
    ) -> RealNumber:
        return divide(left_value, right_value)

    ## Partials and Differentials ##

    def _local_partial(
        self: Divide,
        point: sm.Point,
        variable: str
    ) -> RealNumber:
        left_value = self._left._evaluate(point)
        right_value = self._right._evaluate(point)
        self._verify_domain_constraints(left_value, right_value)
        left_partial = self._left._local_partial(point, variable)
        right_partial = self._right._local_partial(point, variable)
        return add(
            self._local_partial_formula_left(point, left_partial),
            self._local_partial_formula_right(point, right_partial)
        )

    def _synthetic_partial(
        self: Divide,
        variable: str
    ) -> sm.Expression:
        left_partial = self._left._synthetic_partial(variable)
        right_partial = self._right._synthetic_partial(variable)
        return ex.Add(
            self._synthetic_partial_formula_left(left_partial),
            self._synthetic_partial_formula_right(right_partial)
        )

    def _compute_local_differential(
        self: Divide,
        builder: LocalDifferentialBuilder,
        accumulated: RealNumber
    ) -> None:
        left_value = self._left._evaluate(builder.point)
        right_value = self._right._evaluate(builder.point)
        self._verify_domain_constraints(left_value, right_value)
        next_accumulated_left = self._local_partial_formula_left(builder.point, accumulated)
        next_accumulated_right = self._local_partial_formula_right(builder.point, accumulated)
        self._left._compute_local_differential(builder, next_accumulated_left)
        self._right._compute_local_differential(builder, next_accumulated_right)

    def _compute_global_differential(
        self: Divide,
        builder: GlobalDifferentialBuilder,
        accumulated: sm.Expression
    ) -> None:
        next_accumulated_left = self._synthetic_partial_formula_left(accumulated)
        next_accumulated_right = self._synthetic_partial_formula_right(accumulated)
        self._left._compute_global_differential(builder, next_accumulated_left)
        self._right._compute_global_differential(builder, next_accumulated_right)

    def _local_partial_formula_left(
        self: Divide,
        point: sm.Point,
        multiplier: RealNumber
    ) -> RealNumber:
        right_value = self._right._evaluate(point)
        return divide(multiplier, right_value)

    def _synthetic_partial_formula_left(
        self: Divide,
        multiplier: sm.Expression
    ) -> sm.Expression:
        return ex.Divide(multiplier, self._right)

    def _local_partial_formula_right(
        self: Divide,
        point: sm.Point,
        multiplier: RealNumber
    ) -> RealNumber:
        left_value = self._left._evaluate(point)
        right_value = self._right._evaluate(point)
        return multiply(
            negation(divide(left_value, nth_power(right_value, n = 2))),
            multiplier
        )

    def _synthetic_partial_formula_right(
        self: Divide,
        multiplier: sm.Expression
    ) -> sm.Expression:
        return ex.Multiply(
            ex.Negation(ex.Divide(self._left, ex.NthPower(self._right, n = 2))),
            multiplier
        )

    ## Normalization and Reduction ##

    @property
    def _reducers(
        self: Divide
    ) -> list[Callable[[], Optional[sm.Expression]]]:
        return [self._reduce_divide_to_multiplying_with_reciprocal]

    # Divide(u, v) => Multiply(u, Reciprocal(v))
    def _reduce_divide_to_multiplying_with_reciprocal(
        self: Divide
    ) -> Optional[sm.Expression]:
        return ex.Multiply(self._left, ex.Reciprocal(self._right))
