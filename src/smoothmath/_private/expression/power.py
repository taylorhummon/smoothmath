from __future__ import annotations
from typing import TYPE_CHECKING, Callable, Optional
import math
import smoothmath._private.base_expression as base
import smoothmath._private.expression as ex
import smoothmath._private.utilities as util
import smoothmath._private.math_functions as mf
import smoothmath._private.errors as er
if TYPE_CHECKING:
    from smoothmath import RealNumber, Point, Expression
    from smoothmath._private.accumulators import (
        NumericPartialsAccumulator, SyntheticPartialsAccumulator
    )


class Power(base.BinaryExpression):
    """
    A power expression.

    >>> from smoothmath import Point
    >>> from smoothmath.expression import Variable, Power
    >>> Power(Variable("x"), Variable("y")).at(Point(x=2, y=5))
    32

    :param left: the base
    :param right: the exponent
    """

    ## Evaluation ##

    def _verify_domain_constraints(
        self: Power,
        left_value: RealNumber,
        right_value: RealNumber
    ) -> None:
        if left_value == 0:
            if right_value > 0:
                raise er.DomainError("Power(x, y) is not smooth around x = 0 for y > 0")
            elif right_value == 0:
                raise er.DomainError("Power(x, y) is not smooth around (x = 0, y = 0)")
            else: # right_value < 0
                raise er.DomainError("Power(x, y) blows up around x = 0 for y < 0")
        elif left_value < 0:
            raise er.DomainError("Power(x, y) is undefined for x < 0")

    def _value_formula(
        self: Power,
        left_value: RealNumber,
        right_value: RealNumber
    ) -> RealNumber:
        return mf.power(left_value, right_value)

    ## Partials ##

    def _numeric_partial(
        self: Power,
        variable_name: str,
        point: Point
    ) -> RealNumber:
        if (not self._left._variable_names) and self._left._evaluate(point) == 1:
            # If we find something like `Constant(1) ** Whatever`, we can short-circuit.
            return 0
        else:
            left_value = self._left._evaluate(point)
            right_value = self._right._evaluate(point)
            self._verify_domain_constraints(left_value, right_value)
            left_partial = self._left._numeric_partial(variable_name, point)
            right_partial = self._right._numeric_partial(variable_name, point)
            return (
                self._numeric_partial_formula_left(point, left_partial) +
                self._numeric_partial_formula_right(point, right_partial)
            )

    def _synthetic_partial(
        self: Power,
        variable_name: str
    ) -> Expression:
        left_partial = self._left._synthetic_partial(variable_name)
        right_partial = self._right._synthetic_partial(variable_name)
        return ex.Add(
            self._synthetic_partial_formula_left(left_partial),
            self._synthetic_partial_formula_right(right_partial)
        )

    def _compute_numeric_partials(
        self: Power,
        accumulator: NumericPartialsAccumulator,
        multiplier: RealNumber,
        point: Point
    ) -> None:
        if (not self._left._variable_names) and self._left._evaluate(point) == 1:
            # If we find something like `Constant(1) ** Whatever`, we can short-circuit.
            pass
        else:
            left_value = self._left._evaluate(point)
            right_value = self._right._evaluate(point)
            self._verify_domain_constraints(left_value, right_value)
            next_multiplier_left = self._numeric_partial_formula_left(point, multiplier)
            next_multiplier_right = self._numeric_partial_formula_right(point, multiplier)
            self._left._compute_numeric_partials(accumulator, next_multiplier_left, point)
            self._right._compute_numeric_partials(accumulator, next_multiplier_right, point)

    def _compute_synthetic_partials(
        self: Power,
        accumulator: SyntheticPartialsAccumulator,
        multiplier: Expression
    ) -> None:
        next_multiplier_left = self._synthetic_partial_formula_left(multiplier)
        next_multiplier_right = self._synthetic_partial_formula_right(multiplier)
        self._left._compute_synthetic_partials(accumulator, next_multiplier_left)
        self._right._compute_synthetic_partials(accumulator, next_multiplier_right)

    def _numeric_partial_formula_left(
        self: Power,
        point: Point,
        multiplier: RealNumber
    ) -> RealNumber:
        left_value = self._left._evaluate(point)
        right_value = self._right._evaluate(point)
        return mf.multiply(
            right_value,
            mf.power(left_value, mf.minus(right_value, 1)),
            multiplier
        )

    def _synthetic_partial_formula_left(
        self: Power,
        multiplier: Expression
    ) -> Expression:
        return ex.Multiply(
            self._right,
            ex.Power(self._left, ex.Minus(self._right, ex.Constant(1))),
            multiplier
        )

    def _synthetic_partial_formula_right(
        self: Power,
        multiplier: Expression
    ) -> Expression:
        return ex.Multiply(ex.Logarithm(self._left, base = math.e), self, multiplier)

    def _numeric_partial_formula_right(
        self: Power,
        point: Point,
        multiplier: RealNumber
    ) -> RealNumber:
        left_value = self._left._evaluate(point)
        self_value = self._evaluate(point)
        return mf.multiply(mf.logarithm(left_value, base = math.e), self_value, multiplier)

    ## Normalization and Reduction ##

    @property
    def _reducers(
        self: Power
    ) -> list[Callable[[], Optional[Expression]]]:
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
    ) -> Optional[Expression]:
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
    ) -> Optional[Expression]:
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
    ) -> Optional[Expression]:
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
    ) -> Optional[Expression]:
        if isinstance(self._right, ex.Constant):
            n = util.integer_from_integral_real_number(self._right.value)
            if n is not None and n >= 2:
                return ex.NthPower(self._left, n)
        return None

    # Power(u, Constant(-1)) => Reciprocal(u)
    def _reduce_u_to_the_negative_one(
        self: Power
    ) -> Optional[Expression]:
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
    ) -> Optional[Expression]:
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
    ) -> Optional[Expression]:
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
    ) -> Optional[Expression]:
        if isinstance(self._right, ex.Negation):
            return ex.Reciprocal(ex.Power(self._left, self._right._inner))
        else:
            return None

    # Power(Reciprocal(u), v) => Reciprocal(Power(u, v))
    def _reduce_reciprocal_u__to_the_v(
        self: Power
    ) -> Optional[Expression]:
        if isinstance(self._left, ex.Reciprocal):
            return ex.Reciprocal(ex.Power(self._left._inner, self._right))
        else:
            return None
