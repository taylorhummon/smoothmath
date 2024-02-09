from __future__ import annotations
from typing import TYPE_CHECKING, Callable, Optional
import math
import smoothmath as sm
import smoothmath.expression as ex
import smoothmath._private.base_expression as base
from smoothmath._private.utilities import integer_from_integral_real_number
from smoothmath._private.math_functions import logarithm, minus, power, multiply
if TYPE_CHECKING:
    from smoothmath import RealNumber
    from smoothmath._private.local_differential import LocalDifferentialBuilder
    from smoothmath._private.global_differential import GlobalDifferentialBuilder


class Power(base.BinaryExpression):

    ## Evaluation ##

    def _verify_domain_constraints(
        self: Power,
        left_value: RealNumber,
        right_value: RealNumber
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
        left_value: RealNumber,
        right_value: RealNumber
    ) -> RealNumber:
        return power(left_value, right_value)

    ## Partials and Differentials ##

    def _local_partial(
        self: Power,
        point: sm.Point,
        with_respect_to: str
    ) -> RealNumber:
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
        return ex.Add(
            self._synthetic_partial_formula_left(left_partial),
            self._synthetic_partial_formula_right(right_partial)
        )

    def _compute_local_differential(
        self: Power,
        builder: LocalDifferentialBuilder,
        accumulated: RealNumber
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
        multiplier: RealNumber
    ) -> RealNumber:
        left_value = self._left._evaluate(point)
        right_value = self._right._evaluate(point)
        return multiply(
            right_value,
            power(left_value, minus(right_value, 1)),
            multiplier
        )

    def _synthetic_partial_formula_left(
        self: Power,
        multiplier: sm.Expression
    ) -> sm.Expression:
        return ex.Multiply(
            self._right,
            ex.Power(self._left, ex.Minus(self._right, ex.Constant(1))),
            multiplier
        )

    def _local_partial_formula_right(
        self: Power,
        point: sm.Point,
        multiplier: RealNumber
    ) -> RealNumber:
        left_value = self._left._evaluate(point)
        self_value = self._evaluate(point)
        return multiply(logarithm(left_value, base = math.e), self_value, multiplier)

    def _synthetic_partial_formula_right(
        self: Power,
        multiplier: sm.Expression
    ) -> sm.Expression:
        return ex.Multiply(ex.Logarithm(self._left, base = math.e), self, multiplier)

    ## Normalization and Reduction ##

    @property
    def _reducers(
        self: Power
    ) -> list[Callable[[], Optional[sm.Expression]]]:
        return [
            self._reduce_u_to_the_one,
            self._reduce_u_to_the_zero,
            self._reduce_one_to_the_u,
            self._reduce_u_to_the_n_at_least_two,
            self._reduce_u_to_the_negative_one,
            self._reduce_power_with_constant_base,
            self._reduce_power_of_power,
            self._reduce_u_to_the_negation_of_v,
            self._reduce_reciprocal_u__to_the_v
        ]

    # Power(u, Constant(1)) => u
    def _reduce_u_to_the_one(
        self: Power
    ) -> Optional[sm.Expression]:
        if (
            isinstance(self._right, ex.Constant) and
            self._right.value == 1
        ):
            return self._left
        else:
            return None

    # Power(u, Constant(0)) => Constant(1)
    def _reduce_u_to_the_zero(
        self: Power
    ) -> Optional[sm.Expression]:
        if (
            isinstance(self._right, ex.Constant) and
            self._right.value == 0
        ):
            return ex.Constant(1)
        else:
            return None

    # Power(Constant(1), u) => Constant(1)
    def _reduce_one_to_the_u(
        self: Power
    ) -> Optional[sm.Expression]:
        if (
            isinstance(self._left, ex.Constant) and
            self._left.value == 1
        ):
            return ex.Constant(1)
        else:
            return None

    # Power(u, Constant(n)) => NthPower(u, n) when n >= 2
    def _reduce_u_to_the_n_at_least_two(
        self: Power
    ) -> Optional[sm.Expression]:
        if isinstance(self._right, ex.Constant):
            n = integer_from_integral_real_number(self._right.value)
            if n is not None and n >= 2:
                return ex.NthPower(self._left, n)
        return None

    # Power(u, Constant(-1)) => Reciprocal(u)
    def _reduce_u_to_the_negative_one(
        self: Power
    ) -> Optional[sm.Expression]:
        if (
            isinstance(self._right, ex.Constant) and
            self._right.value == -1
        ):
            return ex.Reciprocal(self._left)
        else:
            return None

    # Power(Constant(C), u) => Exponential(u, base = C)
    def _reduce_power_with_constant_base(
        self: Power
    ) -> Optional[sm.Expression]:
        if (
            isinstance(self._left, ex.Constant) and
            self._left.value > 0 and
            self._left.value != 1
        ):
            return ex.Exponential(self._right, base = self._left.value)
        else:
            return None

    # Power(Power(u, v), w) => Power(u, Multiply(v, w))
    def _reduce_power_of_power(
        self: Power
    ) -> Optional[sm.Expression]:
        if isinstance(self._left, ex.Power):
            return ex.Power(
                self._left._left,
                ex.Multiply(self._left._right, self._right)
            )
        else:
            return None

    # Power(u, Negation(v)) => Reciprocal(Power(u, v))
    def _reduce_u_to_the_negation_of_v(
        self: Power
    ) -> Optional[sm.Expression]:
        if isinstance(self._right, ex.Negation):
            return ex.Reciprocal(ex.Power(self._left, self._right._inner))
        else:
            return None

    # Power(Reciprocal(u), v) => Reciprocal(Power(u, v))
    def _reduce_reciprocal_u__to_the_v(
        self: Power
    ) -> Optional[sm.Expression]:
        if isinstance(self._left, ex.Reciprocal):
            return ex.Reciprocal(ex.Power(self._left._inner, self._right))
        else:
            return None
