from __future__ import annotations
from typing import Callable
import smoothmath as sm
import smoothmath.expression as ex
import smoothmath._private.expression.base as base
from smoothmath._private.utilities import integer_from_integral_real_number


def reduce_synthetic(
    expression: sm.Expression
) -> sm.Expression:
    if isinstance(expression, base.NullaryExpression):
        return expression
    elif isinstance(expression, (base.UnaryExpression, base.ParameterizedUnaryExpression)):
        reduced_inner = reduce_synthetic(expression._inner)
        rebuilt = expression._rebuild(reduced_inner)
        return _apply_reducers(rebuilt)
    elif isinstance(expression, base.BinaryExpression):
        reduced_left = reduce_synthetic(expression._left)
        reduced_right = reduce_synthetic(expression._right)
        rebuilt = expression._rebuild(reduced_left, reduced_right)
        return _apply_reducers(rebuilt)
    else:
        raise Exception("internal error: unknown expression kind")


def _apply_reducers(
    expression: sm.Expression
) -> sm.Expression:
    for reducer in reducers:
        reduced_or_none = reducer(expression)
        if reduced_or_none is not None:
            return reduced_or_none
    return expression


###### Reducers ######

### OK to use Constant() below here

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


### OK to use Variable() below here


### OK to use Negation() below here


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


### OK to use Reciprocal() below here


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


# Reciprocal(Negation(u)) => u
def _reduce_reciprocal_of_negation_of_u(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Reciprocal) and
        isinstance(expression._inner, ex.Negation)
    ):
        reduced = _apply_reducers(
            ex.Reciprocal(expression._inner._inner)
        )
        return _apply_reducers(
            ex.Negation(reduced)
        )
    else:
        return None


### OK to use NthPower() below here


# NthPower_m(NthPower_n(u)) => nthPower_{m * n}(u))
def _reduce_mth_power_of_nth_power_of_u(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.NthPower) and
        isinstance(expression._inner, ex.NthPower)
    ):
        return _apply_reducers(
            ex.NthPower(expression._n * expression._inner._n, expression._inner._inner)
        )
    else:
        return None


# NthPower_n(Negation(u)) => NthPower_n(u) where n is even
def _reduce_even_nth_power_of_negation_of_u(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.NthPower) and
        isinstance(expression._inner, ex.Negation) and
        expression._n % 2 == 0
    ):
        return _apply_reducers(
            ex.NthPower(expression._n, expression._inner._inner)
        )
    else:
        return None


# NthPower_n(Negation(u)) => Negation(NthPower_n(u)) where n is odd
def _reduce_odd_nth_power_of_negation_of_u(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.NthPower) and
        isinstance(expression._inner, ex.Negation) and
        expression._n % 2 == 1
    ):
        reduced = _apply_reducers(
            ex.NthPower(expression._n, expression._inner._inner)
        )
        return _apply_reducers(
            ex.Negation(reduced)
        )
    else:
        return None


# NthPower_n(Reciprocal(u)) => Reciprocal(NthPower_n(u))
def _reduce_nth_power_of_reciprocal_of_u(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.NthPower) and
        isinstance(expression._inner, ex.Reciprocal)
    ):
        reduced = _apply_reducers(
            ex.NthPower(expression._n, expression._inner._inner)
        )
        return _apply_reducers(
            ex.Reciprocal(reduced)
        )
    else:
        return None


### OK to use NthRoot() below here


# NthRoot_m(NthRoot_n(u)) => nthRoot_{m * n}(u))
def _reduce_mth_root_of_nth_root_of_u(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.NthRoot) and
        isinstance(expression._inner, ex.NthRoot)
    ):
        return _apply_reducers(
            ex.NthRoot(expression._n * expression._inner._n, expression._inner._inner)
        )
    else:
        return None


# NthRoot_n(Negation(u)) => Negation(NthRoot_n(u)) where n is odd
def _reduce_odd_nth_root_of_negation_of_u(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.NthRoot) and
        isinstance(expression._inner, ex.Negation) and
        expression._n % 2 == 1
    ):
        reduced = _apply_reducers(
            ex.NthRoot(expression._n, expression._inner._inner)
        )
        return _apply_reducers(
            ex.Negation(reduced)
        )
    else:
        return None


# NthRoot_n(Reciprocal(u)) => Reciprocal(NthRoot_n(u))
def _reduce_nth_root_of_reciprocal_of_u(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.NthRoot) and
        isinstance(expression._inner, ex.Reciprocal)
    ):
        reduced = _apply_reducers(
            ex.NthRoot(expression._n, expression._inner._inner)
        )
        return _apply_reducers(
            ex.Reciprocal(reduced)
        )
    else:
        return None


# NthPower(NthRoot(u)) => u
def _reduce_nth_power_of_nth_root_of_u(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.NthPower) and
        isinstance(expression._inner, ex.NthRoot) and
        expression._n == expression._inner._n
    ):
        return expression._inner._inner
    else:
        return None


# NthRoot_n(NthPower_n(u)) => u
def _reduce_nth_root_of_nth_power_of_u(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.NthRoot) and
        isinstance(expression._inner, ex.NthPower) and
        expression._n == expression._inner._n
    ):
        return expression._inner._inner
    else:
        return None


### OK to use Exponential() below here


### OK to use Logarithm() below here


# Logarithm(Exponential(u)) => u
def _reduce_logarithm_of_exponential_of_u(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Logarithm) and
        isinstance(expression._inner, ex.Exponential) and
        expression._base == expression._inner._base
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
        expression._base == expression._inner._base
    ):
        return expression._inner._inner
    else:
        return None


### OK to use Plus() below here


# Plus(Plus(u, v), w) => Plus(u, Plus(v, w))
def _reduce_by_associating_plus_right(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Plus) and
        isinstance(expression._left, ex.Plus)
    ):
        reduced = _apply_reducers(
            ex.Plus(expression._left._right, expression._right)
        )
        return _apply_reducers(
            ex.Plus(expression._left._left, reduced)
        )
    else:
        return None


# Plus(Constant(c), u) => Plus(u, Constant(c))
def _reduce_by_commuting_constants_right_for_plus(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Plus) and
        isinstance(expression._left, ex.Constant) and
        not isinstance(expression._right, ex.Constant) # ensure we make progress
    ):
        return _apply_reducers(
            ex.Plus(expression._right, expression._left)
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
        expression._right._value == 0
    ):
        return expression._left
    else:
        return None


### OK to use Minus() below here


# Minus(u, Constant(0)) => u
def _reduce_u_minus_zero(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Minus) and
        isinstance(expression._right, ex.Constant) and
        expression._right._value == 0
    ):
        return expression._left
    else:
        return None


# Minus(Constant(0), u) => Negation(u)
def _reduce_zero_minus_u(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Minus) and
        isinstance(expression._left, ex.Constant) and
        expression._left._value == 0
    ):
        return _apply_reducers(
            ex.Negation(expression._right)
        )
    else:
        return None


# Negation(Minus(u, v)) => Minus(v, u)
def _reduce_negation_of_u_minus_v(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Negation) and
        isinstance(expression._inner, ex.Minus)
    ):
        return _apply_reducers(
            ex.Minus(expression._inner._right, expression._inner._left)
        )
    else:
        return None


### OK to use Multiply() below here


# Multiply(u, Multiply(v, w)) => Multiply(Multiply(u, v), w)
def _reduce_by_associating_multiply_left(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Multiply) and
        isinstance(expression._right, ex.Multiply)
    ):
        reduced = _apply_reducers(
            ex.Multiply(expression._left, expression._right._left)
        )
        return _apply_reducers(
            ex.Multiply(reduced, expression._right._right)
        )
    else:
        return None


# Multiply(u, Constant(c)) => Multiply(Constant(c), u)
def _reduce_by_commuting_constants_left_for_multiply(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Multiply) and
        isinstance(expression._right, ex.Constant) and
        not isinstance(expression._left, ex.Constant) # ensure we make progress
    ):
        return _apply_reducers(
            ex.Multiply(expression._right, expression._left)
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
        expression._left._value == 1
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
        expression._left._value == 0
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
        expression._left._value == -1
    ):
        return _apply_reducers(
            ex.Negation(expression._right)
        )
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
        reduced = _apply_reducers(
            ex.Multiply(expression._left._inner, expression._right._inner)
        )
        return _apply_reducers(
            ex.Reciprocal(reduced)
        )
    else:
        return None


# Multiply(NthPower_n(u), NthPower_n(v)) => NthPower_n(Multiply(u, v))
def _reduce_product_of_nth_powers(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Multiply) and
        isinstance(expression._left, ex.NthPower) and
        isinstance(expression._right, ex.NthPower) and
        expression._left._n == expression._right._n
    ):
        reduced = _apply_reducers(
            ex.Multiply(expression._left._inner, expression._right._inner)
        )
        return _apply_reducers(
            ex.NthPower(expression._left._n, reduced)
        )
    else:
        return None


# Multiply(NthRoot_n(u), NthRoot_n(v)) => NthRoot_n(Multiply(u, v))
def _reduce_product_of_nth_roots(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Multiply) and
        isinstance(expression._left, ex.NthRoot) and
        isinstance(expression._right, ex.NthRoot) and
        expression._left._n == expression._right._n
    ):
        reduced = _apply_reducers(
            ex.Multiply(expression._left._inner, expression._right._inner)
        )
        return _apply_reducers(
            ex.NthRoot(expression._left._n, reduced)
        )
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
        expression._left._base == expression._right._base
    ):
        reduced = _apply_reducers(
            ex.Plus(expression._left._inner, expression._right._inner)
        )
        return _apply_reducers(
            ex.Exponential(expression._left._base, reduced)
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
        expression._left._base == expression._right._base
    ):
        reduced = _apply_reducers(
            ex.Multiply(expression._left._inner, expression._right._inner)
        )
        return _apply_reducers(
            ex.Logarithm(expression._left._base, reduced)
        )
    else:
        return None


### OK to use Divide() below here


# Divide(u, Constant(1)) => u
def _reduce_u_over_one(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Divide) and
        isinstance(expression._right, ex.Constant) and
        expression._right._value == 1
    ):
        return expression._left
    else:
        return None


# Divide(Constant(1), u) => Reciprocal(u)
def _reduce_one_over_u(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Divide) and
        isinstance(expression._left, ex.Constant) and
        expression._left._value == 1
    ):
        return _apply_reducers(
            ex.Reciprocal(expression._right)
        )
    else:
        return None


# Reciprocal(Divide(u, v)) = Divide(v, u)
def _reduce_reciprocal_of_u_over_v(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Reciprocal) and
        isinstance(expression._inner, ex.Divide)
    ):
        return _apply_reducers(
            ex.Divide(expression._inner._right, expression._inner._left)
        )
    else:
        return None


### OK to use Power() below here


# Power(Constant(1), u) => Constant(1)
def _reduce_one_to_the_u(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Power) and
        isinstance(expression._left, ex.Constant) and
        expression._left._value == 1
    ):
        return ex.Constant(1)
    else:
        return None


# Power(u, Constant(n)) => NthPower(n, u) when n >= 2
def _reduce_u_to_the_n_at_least_two(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Power) and
        isinstance(expression._right, ex.Constant)
    ):
        n = integer_from_integral_real_number(expression._right._value)
        if n is not None and n >= 2:
            return _apply_reducers(
                ex.NthPower(n, expression._left)
            )
    return None


# Power(u, Constant(1)) => u
def _reduce_u_to_the_one(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Power) and
        isinstance(expression._right, ex.Constant) and
        expression._right._value == 1
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
        expression._right._value == 0
    ):
        return ex.Constant(1)
    else:
        return None


# Power(u, Constant(-1)) => Reciprocal(u)
def _reduce_u_to_the_negative_one(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Power) and
        isinstance(expression._right, ex.Constant) and
        expression._right._value == -1
    ):
        return _apply_reducers(
            ex.Reciprocal(expression._left)
        )
    else:
        return None


# Power(u, Constant(0.5)) => NthRoot(2, u)
def _reduce_u_to_the_one_half(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Power) and
        isinstance(expression._right, ex.Constant) and
        expression._right._value == 0.5
    ):
        return _apply_reducers(
            ex.NthRoot(2, expression._left)
        )
    else:
        return None


# Power(Constant(C), u) => Exponential(u, base = C)
def _reduce_power_with_constant_base(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Power) and
        isinstance(expression._left, ex.Constant) and
        expression._left._value > 0 and
        expression._left._value != 1
    ):
        return _apply_reducers(
            ex.Exponential(expression._left._value, expression._right)
        )
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
        reduced = _apply_reducers(
            ex.Multiply(expression._left._right, expression._right)
        )
        return _apply_reducers(
            ex.Power(expression._left._left, reduced)
        )
    else:
        return None


reducers: list[Callable[[sm.Expression], sm.Expression | None]]
reducers = [
    # Constant() OK
    _reduce_expressions_that_lack_variables,
    # Variable() OK
    # Negation() OK
    _reduce_negation_of_negation_of_u,
    # Reciprocal() OK
    _reduce_reciprocal_of_reciprocal_of_u,
    _reduce_reciprocal_of_negation_of_u,
    # NthPower() OK
    _reduce_mth_power_of_nth_power_of_u,
    _reduce_even_nth_power_of_negation_of_u,
    _reduce_odd_nth_power_of_negation_of_u,
    _reduce_nth_power_of_reciprocal_of_u,
    # NthRoot() OK
    _reduce_mth_root_of_nth_root_of_u,
    _reduce_odd_nth_root_of_negation_of_u,
    _reduce_nth_root_of_reciprocal_of_u,
    _reduce_nth_power_of_nth_root_of_u,
    _reduce_nth_root_of_nth_power_of_u,
    # Exponential() OK
    # Logarithm() OK
    _reduce_logarithm_of_exponential_of_u,
    _reduce_exponential_of_logarithm_of_u,
    # Plus() OK
    _reduce_by_associating_plus_right,
    _reduce_by_commuting_constants_right_for_plus,
    _reduce_u_plus_zero,
    # Minus() OK
    _reduce_u_minus_zero,
    _reduce_zero_minus_u,
    _reduce_negation_of_u_minus_v,
    # Multiply() OK
    _reduce_by_associating_multiply_left,
    _reduce_by_commuting_constants_left_for_multiply,
    _reduce_one_times_u,
    _reduce_zero_times_u,
    _reduce_negative_one_times_u,
    _reduce_product_of_reciprocals,
    _reduce_product_of_nth_powers,
    _reduce_product_of_nth_roots,
    _reduce_product_of_exponentials,
    _reduce_sum_of_logarithms,
    # Divide() OK
    _reduce_u_over_one,
    _reduce_one_over_u,
    _reduce_reciprocal_of_u_over_v,
    # Power() OK
    _reduce_one_to_the_u,
    _reduce_u_to_the_n_at_least_two,
    _reduce_u_to_the_one,
    _reduce_u_to_the_zero,
    _reduce_u_to_the_negative_one,
    _reduce_u_to_the_one_half,
    _reduce_power_with_constant_base,
    _reduce_power_of_power
]
