from __future__ import annotations
from typing import Callable
import math
import smoothmath as sm
import smoothmath.expression as ex
import smoothmath._private.expression.base as base
from smoothmath._private.utilities import integer_from_integral_real_number


# We can assume that all inner subexpressions are fully reduced.
# Our job is to either make a reduction or mark the outer expression as fully reduced.
def apply_reducer_or_mark_as_fully_reduced(
    expression: sm.Expression
) -> sm.Expression:
    for reducer in reducers:
        reduced_or_none = reducer(expression)
        if reduced_or_none is not None:
            return reduced_or_none
    expression._is_fully_reduced = True
    return expression


def _reduce_expressions_that_lack_variables(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        expression._lacks_variables and
        not isinstance(expression, base.NullaryExpression)
    ):
        try:
            value = expression.evaluate(sm.Point({}))
            return ex.Constant(value)
        except sm.DomainError:
            return None
    else:
        return None


### Negation and Reciprocal Reducers ###


# Negation(Negation(u)) => u
def _reduce_negation_of_negation_of_u(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Negation) and
        isinstance(expression._inner, ex.Negation)
    ):
        return expression._inner._inner
    else:
        return None


# Reciprocal(Reciprocal(u)) => u
def _reduce_reciprocal_of_reciprocal_of_u(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Reciprocal) and
        isinstance(expression._inner, ex.Reciprocal)
    ):
        return expression._inner._inner
    else:
        return None


# Reciprocal(Negation(u)) => Negation(Reciprocal(u))
def _reduce_reciprocal_of_negation_of_u(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Reciprocal) and
        isinstance(expression._inner, ex.Negation)
    ):
        return ex.Negation(ex.Reciprocal(expression._inner._inner))
    else:
        return None


### Plus Reducers ###


# Plus(Plus(u, v), w) => Plus(u, Plus(v, w))
def _reduce_by_associating_plus_right(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Plus) and
        isinstance(expression._left, ex.Plus)
    ):
        return ex.Plus(
            expression._left._left,
            ex.Plus(expression._left._right, expression._right)
        )
    else:
        return None


# Plus(u, Constant(0)) => u
def _reduce_u_plus_zero(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Plus) and
        isinstance(expression._right, ex.Constant) and
        expression._right.value == 0
    ):
        return expression._left
    else:
        return None


# Plus(Constant(c), u) => Plus(u, Constant(c))
def _reduce_by_commuting_constant_right_across_plus(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Plus) and
        isinstance(expression._left, ex.Constant) and
        not isinstance(expression._right, (ex.Constant, ex.Negation))
    ):
        return ex.Plus(expression._right, expression._left)
    else:
        return None


# Plus(Negation(u), v) => Plus(v, Negation(u))
def _reduce_by_commuting_negation_right_across_plus(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Plus) and
        isinstance(expression._left, ex.Negation) and
        not isinstance(expression._right, ex.Negation)
    ):
        return ex.Plus(expression._right, expression._left)
    else:
        return None


# Plus(Negation(u), Negation(v)) => Negation(Plus(u, v))
def _reduce_sum_of_negations(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Plus) and
        isinstance(expression._left, ex.Negation) and
        isinstance(expression._right, ex.Negation)
    ):
        return ex.Negation(ex.Plus(expression._left._inner, expression._right._inner))
    else:
        return None


### Multiply Reducers ###


# Multiply(u, Multiply(v, w)) => Multiply(Multiply(u, v), w)
def _reduce_by_associating_multiply_left(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Multiply) and
        isinstance(expression._right, ex.Multiply)
    ):
        return ex.Multiply(
            ex.Multiply(expression._left, expression._right._left),
            expression._right._right
        )
    else:
        return None


# Multiply(Constant(1), u) => u
def _reduce_one_times_u(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Multiply) and
        isinstance(expression._left, ex.Constant) and
        expression._left.value == 1
    ):
        return expression._right
    else:
        return None


# Multiply(Constant(0), u) => Constant(0)
def _reduce_zero_times_u(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Multiply) and
        isinstance(expression._left, ex.Constant) and
        expression._left.value == 0
    ):
        return ex.Constant(0)
    else:
        return None


# Multiply(Constant(-1), u) => Negation(u)
def _reduce_negative_one_times_u(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Multiply) and
        isinstance(expression._left, ex.Constant) and
        expression._left.value == -1
    ):
        return ex.Negation(expression._right)
    else:
        return None


# Multiply(u, Constant(c)) => Multiply(Constant(c), u)
def _reduce_by_commuting_constant_left_across_multiply(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Multiply) and
        isinstance(expression._right, ex.Constant) and
        not isinstance(expression._left, (ex.Constant, ex.Reciprocal, ex.Multiply))
    ):
        return ex.Multiply(expression._right, expression._left)
    else:
        return None


# Multiply(Negation(u), v) => Negation(Multiply(u, v))
def _reduce_negation_of_u__times_v(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Multiply) and
        isinstance(expression._left, ex.Negation)
    ):
        return ex.Negation(ex.Multiply(expression._left._inner, expression._right))
    else:
        return None


# Multiply(u, Negation(v)) => Negation(Multiply(u, v))
def _reduce_u_times_negation_of_v(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Multiply) and
        isinstance(expression._right, ex.Negation)
    ):
        return ex.Negation(ex.Multiply(expression._left, expression._right._inner))
    else:
        return None


# Multiply(u, Reciprocal(v)) => Multiply(Reciprocal(v), u)
def _reduce_by_commuting_reciprocal_left_across_multiply(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Multiply) and
        isinstance(expression._right, ex.Reciprocal) and
        not isinstance(expression._left, (ex.Reciprocal, ex.Multiply))
    ):
        return ex.Multiply(expression._right, expression._left)
    else:
        return None


# Multiply(Reciprocal(u), Reciprocal(v)) => Reciprocal(Multiply(u, v))
def _reduce_product_of_reciprocals(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Multiply) and
        isinstance(expression._left, ex.Reciprocal) and
        isinstance(expression._right, ex.Reciprocal)
    ):
        return ex.Reciprocal(ex.Multiply(expression._left._inner, expression._right._inner))
    else:
        return None


### Cosine and Sine Reducers ###


# Cosine(Negation(u)) => Cosine(u)
def _reduce_cosine_of_negation_of_u(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Cosine) and
        isinstance(expression._inner, ex.Negation)
    ):
        return ex.Cosine(expression._inner._inner)
    else:
        return None


# Sine(Negation(u)) => Sine(u)
def _reduce_sine_of_negation_of_u(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Sine) and
        isinstance(expression._inner, ex.Negation)
    ):
        return ex.Negation(ex.Sine(expression._inner._inner))
    else:
        return None


### NthPower and NthRoot Reducers ###


# NthPower(u, 1) => u
def _reduce_nth_power_where_n_is_one(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.NthPower) and
        expression.n == 1
    ):
        return expression._inner
    else:
        return None


# NthRoot(u, 1) => u
def _reduce_nth_root_where_n_is_one(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.NthRoot) and
        expression.n == 1
    ):
        return expression._inner
    else:
        return None


# NthPower(NthRoot(u, m), n) => ...
def _reduce_nth_power_of_mth_root_of_u(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.NthPower) and
        isinstance(expression._inner, ex.NthRoot)
    ):
        n = expression.n
        m = expression._inner.n
        if m == n:
            return expression._inner._inner
        greatest_common_divisor = math.gcd(m, n)
        if greatest_common_divisor != 1:
            return ex.NthPower(
                ex.NthRoot(expression._inner._inner, m // greatest_common_divisor),
                n // greatest_common_divisor
            )
    else:
        return None


# NthRoot(NthPower(u, m), n) => NthPower(NthRoot(u, n), m)
def _reduce_nth_root_of_mth_power_of_u(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.NthRoot) and
        isinstance(expression._inner, ex.NthPower)
    ):
        return ex.NthPower(
            ex.NthRoot(expression._inner._inner, expression.n),
            expression._inner.n
        )
    else:
        return None


# Multiply(NthPower(u, n), NthPower(v, n)) => NthPower(Multiply(u, v), n)
def _reduce_product_of_nth_powers(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Multiply) and
        isinstance(expression._left, ex.NthPower) and
        isinstance(expression._right, ex.NthPower) and
        expression._left.n == expression._right.n
    ):
        return ex.NthPower(
            ex.Multiply(expression._left._inner, expression._right._inner),
            expression._left.n
        )
    else:
        return None


# Multiply(NthRoot(u, n), NthRoot(v, n)) => NthRoot(Multiply(u, v), n)
def _reduce_product_of_nth_roots(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Multiply) and
        isinstance(expression._left, ex.NthRoot) and
        isinstance(expression._right, ex.NthRoot) and
        expression._left.n == expression._right.n
    ):
        return ex.NthRoot(
            ex.Multiply(expression._left._inner, expression._right._inner),
            expression._left.n
        )
    else:
        return None


# NthPower(NthPower(u, m), n) => NthPower(u, m * n))
def _reduce_nth_power_of_mth_power_of_u(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.NthPower) and
        isinstance(expression._inner, ex.NthPower)
    ):
        return ex.NthPower(expression._inner._inner, expression.n * expression._inner.n)
    else:
        return None


# NthRoot(NthRoot(u, m), n) => NthRoot(u, m * n))
def _reduce_nth_root_of_mth_root_of_u(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.NthRoot) and
        isinstance(expression._inner, ex.NthRoot)
    ):
        return ex.NthRoot(expression._inner._inner, expression.n * expression._inner.n)
    else:
        return None


# NthPower(Negation(u), n) => NthPower(u, n) when n is even
# NthPower(Negation(u), n) => Negation(NthPower(u, n)) when n is odd
def _reduce_nth_power_of_negation_of_u(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.NthPower) and
        isinstance(expression._inner, ex.Negation)
    ):
        if expression.n % 2 == 0: # n is even
            return ex.NthPower(expression._inner._inner, expression.n)
        else: # n is odd
            return ex.Negation(ex.NthPower(expression._inner._inner, expression.n))
    else:
        return None


# NthRoot(Negation(u), n) => Negation(NthRoot(u, n)) where n is odd
def _reduce_odd_nth_root_of_negation_of_u(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.NthRoot) and
        isinstance(expression._inner, ex.Negation) and
        expression.n % 2 == 1
    ):
        return ex.Negation(ex.NthRoot(expression._inner._inner, expression.n))
    else:
        return None


# NthPower(Reciprocal(u), n) => Reciprocal(NthPower(u, n))
def _reduce_nth_power_of_reciprocal_of_u(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.NthPower) and
        isinstance(expression._inner, ex.Reciprocal)
    ):
        return ex.Reciprocal(ex.NthPower(expression._inner._inner, expression.n))
    else:
        return None


# NthRoot(Reciprocal(u), n) => Reciprocal(NthRoot(u, n))
def _reduce_nth_root_of_reciprocal_of_u(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.NthRoot) and
        isinstance(expression._inner, ex.Reciprocal)
    ):
        return ex.Reciprocal(ex.NthRoot(expression._inner._inner, expression.n))
    else:
        return None


### Exponential and Logarithm Reducers ###


# Logarithm(Exponential(u)) => u
def _reduce_logarithm_of_exponential_of_u(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Logarithm) and
        isinstance(expression._inner, ex.Exponential) and
        expression.base == expression._inner.base
    ):
        return expression._inner._inner
    else:
        return None


# Exponential(Logarithm(u)) => u
def _reduce_exponential_of_logarithm_of_u(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Exponential) and
        isinstance(expression._inner, ex.Logarithm) and
        expression.base == expression._inner.base
    ):
        return expression._inner._inner
    else:
        return None


# Multiply(Exponential(u), Exponential(v)) => Exponential(Plus(u, v))
def _reduce_product_of_exponentials(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Multiply) and
        isinstance(expression._left, ex.Exponential) and
        isinstance(expression._right, ex.Exponential) and
        expression._left.base == expression._right.base
    ):
        return ex.Exponential(
            ex.Plus(expression._left._inner, expression._right._inner),
            base = expression._left.base
        )
    else:
        return None


# Plus(Logarithm(u), Logarithm(v)) => Logarithm(Multiply(u, v))
def _reduce_sum_of_logarithms(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Plus) and
        isinstance(expression._left, ex.Logarithm) and
        isinstance(expression._right, ex.Logarithm) and
        expression._left.base == expression._right.base
    ):
        return ex.Logarithm(
            ex.Multiply(expression._left._inner, expression._right._inner),
            base = expression._left.base
        )
    else:
        return None


# Exponential(Negation(u)) => Reciprocal(Exponential(u))
def _reduce_exponential_of_negation_of_u(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Exponential) and
        isinstance(expression._inner, ex.Negation)
    ):
        return ex.Reciprocal(ex.Exponential(expression._inner._inner, base = expression.base))
    else:
        return None


# Logarithm(Reciprocal(u)) => Negation(Logarithm(u))
def _reduce_logarithm_of_reciprocal_of_u(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Logarithm) and
        isinstance(expression._inner, ex.Reciprocal)
    ):
        return ex.Negation(ex.Logarithm(expression._inner._inner, base = expression.base))
    else:
        return None


# NthPower(Exponential(u), n) => Exponential(Multiply(Constant(n), u))
def _reduce_nth_power_of_exponential_of_u(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.NthPower) and
        isinstance(expression._inner, ex.Exponential)
    ):
        return ex.Exponential(
            ex.Multiply(ex.Constant(expression.n), expression._inner._inner),
            base = expression._inner.base
        )
    else:
        return None


# Logarithm(NthPower(u, n)) = Multiply(Constant(n), Logarithm(u)) when n is odd
def _reduce_logarithm_of_nth_power_of_u(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Logarithm) and
        isinstance(expression._inner, ex.NthPower) and
        expression._inner.n % 2 == 1
    ):
        return ex.Multiply(
            ex.Constant(expression._inner.n),
            ex.Logarithm(expression._inner._inner, base = expression.base)
        )
    else:
        return None


### Power Reducers ###


# Power(u, Constant(1)) => u
def _reduce_u_to_the_one(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Power) and
        isinstance(expression._right, ex.Constant) and
        expression._right.value == 1
    ):
        return expression._left
    else:
        return None


# Power(u, Constant(0)) => Constant(1)
def _reduce_u_to_the_zero(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Power) and
        isinstance(expression._right, ex.Constant) and
        expression._right.value == 0
    ):
        return ex.Constant(1)
    else:
        return None


# Power(Constant(1), u) => Constant(1)
def _reduce_one_to_the_u(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Power) and
        isinstance(expression._left, ex.Constant) and
        expression._left.value == 1
    ):
        return ex.Constant(1)
    else:
        return None


# Power(u, Constant(n)) => NthPower(u, n) when n >= 2
def _reduce_u_to_the_n_at_least_two(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Power) and
        isinstance(expression._right, ex.Constant)
    ):
        n = integer_from_integral_real_number(expression._right.value)
        if n is not None and n >= 2:
            return ex.NthPower(expression._left, n)
    return None


# Power(u, Constant(-1)) => Reciprocal(u)
def _reduce_u_to_the_negative_one(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Power) and
        isinstance(expression._right, ex.Constant) and
        expression._right.value == -1
    ):
        return ex.Reciprocal(expression._left)
    else:
        return None


# Power(u, Reciprocal(Constant(n))) => NthRoot(u, n) when n >= 1
def _reduce_u_to_the_one_over_n(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Power) and
        isinstance(expression._right, ex.Reciprocal) and
        isinstance(expression._right._inner, ex.Constant)
    ):
        n = integer_from_integral_real_number(expression._right._inner.value)
        if n is not None and n >= 1:
            return ex.NthRoot(expression._left, n)
    else:
        return None


# Power(Constant(C), u) => Exponential(u, base = C)
def _reduce_power_with_constant_base(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Power) and
        isinstance(expression._left, ex.Constant) and
        expression._left.value > 0 and
        expression._left.value != 1
    ):
        return ex.Exponential(expression._right, base = expression._left.value)
    else:
        return None


# Power(Power(u, v), w) => Power(u, Multiply(v, w))
def _reduce_power_of_power(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Power) and
        isinstance(expression._left, ex.Power)
    ):
        return ex.Power(
            expression._left._left,
            ex.Multiply(expression._left._right, expression._right)
        )
    else:
        return None


# Power(u, Negation(v)) => Reciprocal(Power(u, v))
def _reduce_u_to_the_negation_of_v(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Power) and
        isinstance(expression._right, ex.Negation)
    ):
        return ex.Reciprocal(ex.Power(expression._left, expression._right._inner))
    else:
        return None


# Power(Reciprocal(u), v) => Reciprocal(Power(u, v))
def _reduce_one_over_u__to_the_v(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Power) and
        isinstance(expression._left, ex.Reciprocal)
    ):
        return ex.Reciprocal(ex.Power(expression._left._inner, expression._right))
    else:
        return None


reducers: list[Callable[[sm.Expression], sm.Expression | None]]
reducers = [
    _reduce_expressions_that_lack_variables,
    # Negation and Reciprocal
    _reduce_negation_of_negation_of_u,
    _reduce_reciprocal_of_reciprocal_of_u,
    _reduce_reciprocal_of_negation_of_u,
    # Plus
    _reduce_by_associating_plus_right,
    _reduce_u_plus_zero,
    _reduce_by_commuting_constant_right_across_plus,
    _reduce_by_commuting_negation_right_across_plus,
    _reduce_sum_of_negations,
    # Multiply
    _reduce_by_associating_multiply_left,
    _reduce_one_times_u,
    _reduce_zero_times_u,
    _reduce_negative_one_times_u,
    _reduce_by_commuting_constant_left_across_multiply,
    _reduce_negation_of_u__times_v,
    _reduce_u_times_negation_of_v,
    _reduce_by_commuting_reciprocal_left_across_multiply,
    _reduce_product_of_reciprocals,
    # Cosine and Sine
    _reduce_cosine_of_negation_of_u,
    _reduce_sine_of_negation_of_u,
    # NthPower and NthRoot
    _reduce_nth_power_where_n_is_one,
    _reduce_nth_root_where_n_is_one,
    _reduce_nth_power_of_mth_root_of_u,
    _reduce_nth_root_of_mth_power_of_u,
    _reduce_product_of_nth_powers,
    _reduce_product_of_nth_roots,
    _reduce_nth_power_of_mth_power_of_u,
    _reduce_nth_root_of_mth_root_of_u,
    _reduce_nth_power_of_negation_of_u,
    _reduce_odd_nth_root_of_negation_of_u,
    _reduce_nth_power_of_reciprocal_of_u,
    _reduce_nth_root_of_reciprocal_of_u,
    # Exponential and Logarithm
    _reduce_logarithm_of_exponential_of_u,
    _reduce_exponential_of_logarithm_of_u,
    _reduce_product_of_exponentials,
    _reduce_sum_of_logarithms,
    _reduce_exponential_of_negation_of_u,
    _reduce_logarithm_of_reciprocal_of_u,
    _reduce_nth_power_of_exponential_of_u,
    _reduce_logarithm_of_nth_power_of_u,
    # Power
    _reduce_u_to_the_one,
    _reduce_u_to_the_zero,
    _reduce_one_to_the_u,
    _reduce_u_to_the_n_at_least_two,
    _reduce_u_to_the_negative_one,
    _reduce_u_to_the_one_over_n,
    _reduce_power_with_constant_base,
    _reduce_power_of_power,
    _reduce_u_to_the_negation_of_v,
    _reduce_one_over_u__to_the_v
]
