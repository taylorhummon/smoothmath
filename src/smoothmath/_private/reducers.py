from __future__ import annotations
from typing import Callable
import smoothmath as sm
import smoothmath.expression as ex
import smoothmath._private.expression.base as base


def reduce_synthetic(
    expression: sm.Expression
) -> sm.Expression:
    if isinstance(expression, base.BinaryExpression):
        reduced_a = reduce_synthetic(expression._a)
        reduced_b = reduce_synthetic(expression._b)
        rebuilt = expression._rebuild(reduced_a, reduced_b)
        return _apply_reducers(rebuilt)
    elif isinstance(expression, base.UnaryExpression):
        reduced_a = reduce_synthetic(expression._a)
        rebuilt = expression._rebuild(reduced_a)
        return _apply_reducers(rebuilt)
    else: # expression is an instance of base.NullaryExpression
        return expression


def _apply_reducers(
    expression: sm.Expression
) -> sm.Expression:
    for reducer in reducers:
        reduced_or_none = reducer(expression)
        if reduced_or_none is not None:
            return reduced_or_none
    return expression


### Reducers ###


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


# Negation(Negation(u)) => u
def _reduce_negation_of_negation_of_u(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Negation) and
        isinstance(expression._a, ex.Negation)
    ):
        return expression._a._a
    else:
        return None


# Reciprocal(Reciprocal(u)) => u
def _reduce_reciprocal_of_reciprocal_of_u(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Reciprocal) and
        isinstance(expression._a, ex.Reciprocal)
    ):
        return expression._a._a
    else:
        return None


# Multiply(Reciprocal(u), Reciprocal(v)) => Reciprocal(Multiply(u, v))
def _reduce_product_of_reciprocals(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Multiply) and
        isinstance(expression._a, ex.Reciprocal) and
        isinstance(expression._b, ex.Reciprocal)
    ):
        inner = _apply_reducers(
            ex.Multiply(expression._a._a, expression._b._a)
        )
        return _apply_reducers(
            ex.Reciprocal(inner)
        )
    else:
        return None


# Square(Negation(u)) => Square(u)
def _reduce_square_of_negation_of_u(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Square) and
        isinstance(expression._a, ex.Negation)
    ):
        return _apply_reducers(
            ex.Square(expression._a._a)
        )
    else:
        return None


# Square(Reciprocal(u)) => Reciprocal(Square(u))
def _reduce_square_of_reciprocal_of_u(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Square) and
        isinstance(expression._a, ex.Reciprocal)
    ):
        inner = _apply_reducers(
            ex.Square(expression._a._a)
        )
        return _apply_reducers(
            ex.Reciprocal(inner)
        )
    else:
        return None


# Multiply(Square(u), Square(v)) => Square(Multiply(u, v))
def _reduce_product_of_squares(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Multiply) and
        isinstance(expression._a, ex.Square) and
        isinstance(expression._b, ex.Square)
    ):
        inner = _apply_reducers(
            ex.Multiply(expression._a._a, expression._b._a)
        )
        return _apply_reducers(
            ex.Square(inner)
        )
    else:
        return None


# Square(SquareRoot(u)) => u
def _reduce_square_of_square_root_of_u(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Square) and
        isinstance(expression._a, ex.SquareRoot)
    ):
        return expression._a._a
    else:
        return None


# SquareRoot(Square(u)) => u
def _reduce_square_root_of_square_of_u(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.SquareRoot) and
        isinstance(expression._a, ex.Square)
    ):
        return expression._a._a
    else:
        return None


# SquareRoot(Reciprocal(u)) => Reciprocal(SquareRoot(u))
def _reduce_square_root_of_reciprocal_of_u(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.SquareRoot) and
        isinstance(expression._a, ex.Reciprocal)
    ):
        inner = _apply_reducers(
            ex.SquareRoot(expression._a._a)
        )
        return _apply_reducers(
            ex.Reciprocal(inner)
        )
    else:
        return None


# Multiply(SquareRoot(u), SquareRoot(v)) => SquareRoot(Multiply(u, v))
def _reduce_product_of_square_roots(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Multiply) and
        isinstance(expression._a, ex.SquareRoot) and
        isinstance(expression._b, ex.SquareRoot)
    ):
        inner = _apply_reducers(
            ex.Multiply(expression._a._a, expression._b._a)
        )
        return _apply_reducers(
            ex.SquareRoot(inner)
        )
    else:
        return None


# Multiply(Exponential(u), Exponential(v)) => Exponential(Plus(u, v))
def _reduce_product_of_exponentials(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Multiply) and
        isinstance(expression._a, ex.Exponential) and
        isinstance(expression._b, ex.Exponential) and
        expression._a._base == expression._b._base
    ):
        inner = _apply_reducers(
            ex.Plus(expression._a._a, expression._b._a)
        )
        return _apply_reducers(
            ex.Exponential(expression._a._base, inner)
        )
    else:
        return None


# Plus(Logarithm(u), Logarithm(v)) => Logarithm(Multiply(u, v))
def _reduce_sum_of_logarithms(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Plus) and
        isinstance(expression._a, ex.Logarithm) and
        isinstance(expression._b, ex.Logarithm) and
        expression._a._base == expression._b._base
    ):
        inner = _apply_reducers(
            ex.Multiply(expression._a._a, expression._b._a)
        )
        return _apply_reducers(
            ex.Logarithm(expression._a._base, inner)
        )
    else:
        return None


# Logarithm(Exponential(u)) => u
def _reduce_logarithm_of_exponential_of_u(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Logarithm) and
        isinstance(expression._a, ex.Exponential) and
        expression._base == expression._a._base
    ):
        return expression._a._a
    else:
        return None


# Exponential(Logarithm(u)) => u
def _reduce_exponential_of_logarithm_of_u(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Exponential) and
        isinstance(expression._a, ex.Logarithm) and
        expression._base == expression._a._base
    ):
        return expression._a._a
    else:
        return None


# Plus(Plus(u, v), w) => Plus(u, Plus(v, w))
def _reduce_by_associating_plus_right(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Plus) and
        isinstance(expression._a, ex.Plus)
    ):
        inner = _apply_reducers(
            ex.Plus(expression._a._b, expression._b)
        )
        return _apply_reducers(
            ex.Plus(expression._a._a, inner)
        )
    else:
        return None


# Plus(Constant(c), u) => Plus(u, Constant(c))
def _reduce_by_commuting_constants_right_for_plus(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Plus) and
        isinstance(expression._a, ex.Constant) and
        not isinstance(expression._b, ex.Constant) # ensure we make progress
    ):
        return _apply_reducers(
            ex.Plus(expression._b, expression._a)
        )
    else:
        return None


# Plus(u, Constant(0)) => u
def _reduce_u_plus_zero(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Plus) and
        isinstance(expression._b, ex.Constant) and
        expression._b._value == 0
    ):
        return expression._a
    else:
        return None


# Minus(u, Constant(0)) => u
def _reduce_u_minus_zero(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Minus) and
        isinstance(expression._b, ex.Constant) and
        expression._b._value == 0
    ):
        return expression._a
    else:
        return None


# Minus(Constant(0), u) => Negation(u)
def _reduce_zero_minus_u(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Minus) and
        isinstance(expression._a, ex.Constant) and
        expression._a._value == 0
    ):
        return _apply_reducers(
            ex.Negation(expression._b)
        )
    else:
        return None


# Negation(Minus(u, v)) => Minus(v, u)
def _reduce_negation_of_u_minus_v(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Negation) and
        isinstance(expression._a, ex.Minus)
    ):
        return _apply_reducers(
            ex.Minus(expression._a._b, expression._a._a)
        )
    else:
        return None


# Multiply(u, Multiply(v, w)) => Multiply(Multiply(u, v), w)
def _reduce_by_associating_multiply_left(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Multiply) and
        isinstance(expression._b, ex.Multiply)
    ):
        inner = ex.Multiply(expression._a, expression._b._a)
        reduced_inner = _apply_reducers(inner)
        return _apply_reducers(
            ex.Multiply(reduced_inner, expression._b._b)
        )
    else:
        return None


# Multiply(u, Constant(c)) => Multiply(Constant(c), u)
def _reduce_by_commuting_constants_left_for_multiply(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Multiply) and
        isinstance(expression._b, ex.Constant) and
        not isinstance(expression._a, ex.Constant) # ensure we make progress
    ):
        return _apply_reducers(
            ex.Multiply(expression._b, expression._a)
        )
    else:
        return None


# Multiply(Constant(1), u) => u
def _reduce_one_times_u(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Multiply) and
        isinstance(expression._a, ex.Constant) and
        expression._a._value == 1
    ):
        return expression._b
    else:
        return None


# Multiply(Constant(0), u) => Constant(0)
def _reduce_zero_times_u(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Multiply) and
        isinstance(expression._a, ex.Constant) and
        expression._a._value == 0
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
        isinstance(expression._a, ex.Constant) and
        expression._a._value == -1
    ):
        return _apply_reducers(
            ex.Negation(expression._b)
        )
    else:
        return None


# Divide(u, Constant(1)) => u
def _reduce_u_over_one(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Divide) and
        isinstance(expression._b, ex.Constant) and
        expression._b._value == 1
    ):
        return expression._a
    else:
        return None


# Divide(Constant(1), u) => Reciprocal(u)
def _reduce_one_over_u(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Divide) and
        isinstance(expression._a, ex.Constant) and
        expression._a._value == 1
    ):
        return _apply_reducers(
            ex.Reciprocal(expression._b)
        )
    else:
        return None


# Reciprocal(Divide(u, v)) = Divide(v, u)
def _reduce_reciprocal_of_u_over_v(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Reciprocal) and
        isinstance(expression._a, ex.Divide)
    ):
        return _apply_reducers(
            ex.Divide(expression._a._b, expression._a._a)
        )
    else:
        return None


# Power(Constant(1), u) => Constant(1)
def _reduce_one_to_the_u(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Power) and
        isinstance(expression._a, ex.Constant) and
        expression._a._value == 1
    ):
        return ex.Constant(1)
    else:
        return None


# Power(u, Constant(2)) => Square(u)
def _reduce_u_to_the_two(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Power) and
        isinstance(expression._b, ex.Constant) and
        expression._b._value == 2
    ):
        return _apply_reducers(
            ex.Square(expression._a)
        )
    else:
        return None


# Power(u, Constant(1)) => u
def _reduce_u_to_the_one(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Power) and
        isinstance(expression._b, ex.Constant) and
        expression._b._value == 1
    ):
        return expression._a
    else:
        return None


# Power(u, Constant(0)) => Constant(1)
def _reduce_u_to_the_zero(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Power) and
        isinstance(expression._b, ex.Constant) and
        expression._b._value == 0
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
        isinstance(expression._b, ex.Constant) and
        expression._b._value == -1
    ):
        return _apply_reducers(
            ex.Reciprocal(expression._a)
        )
    else:
        return None


# Power(u, Constant(0.5)) => Reciprocal(u)
def _reduce_u_to_the_one_half(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Power) and
        isinstance(expression._b, ex.Constant) and
        expression._b._value == 0.5
    ):
        return _apply_reducers(
            ex.SquareRoot(expression._a)
        )
    else:
        return None


# Power(Constant(C), u) => Exponential(u, base = C)
def _reduce_power_with_constant_base(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Power) and
        isinstance(expression._a, ex.Constant) and
        expression._a._value > 0 and
        expression._a._value != 1
    ):
        return _apply_reducers(
            ex.Exponential(expression._a._value, expression._b)
        )
    else:
        return None


# Power(Power(u, v), w) => Power(u, Multiply(v, w))
def _reduce_power_of_power(
    expression: sm.Expression
) -> sm.Expression | None:
    if (
        isinstance(expression, ex.Power) and
        isinstance(expression._a, ex.Power)
    ):
        inner = _apply_reducers(
            ex.Multiply(expression._a._b, expression._b)
        )
        return _apply_reducers(
            ex.Power(expression._a._a, inner)
        )
    else:
        return None


reducers: list[Callable[[sm.Expression], sm.Expression | None]]
reducers = [
    _reduce_expressions_that_lack_variables,
    _reduce_negation_of_negation_of_u,
    _reduce_reciprocal_of_reciprocal_of_u,
    _reduce_product_of_reciprocals,
    _reduce_square_of_negation_of_u,
    _reduce_square_of_reciprocal_of_u,
    _reduce_product_of_squares,
    _reduce_square_of_square_root_of_u,
    _reduce_square_root_of_square_of_u,
    _reduce_square_root_of_reciprocal_of_u,
    _reduce_product_of_square_roots,
    _reduce_product_of_exponentials,
    _reduce_sum_of_logarithms,
    _reduce_logarithm_of_exponential_of_u,
    _reduce_exponential_of_logarithm_of_u,
    _reduce_by_associating_plus_right,
    _reduce_by_commuting_constants_right_for_plus,
    _reduce_u_plus_zero,
    _reduce_u_minus_zero,
    _reduce_zero_minus_u,
    _reduce_negation_of_u_minus_v,
    _reduce_by_associating_multiply_left,
    _reduce_by_commuting_constants_left_for_multiply,
    _reduce_one_times_u,
    _reduce_zero_times_u,
    _reduce_negative_one_times_u,
    _reduce_u_over_one,
    _reduce_one_over_u,
    _reduce_reciprocal_of_u_over_v,
    _reduce_one_to_the_u,
    _reduce_u_to_the_two,
    _reduce_u_to_the_one,
    _reduce_u_to_the_zero,
    _reduce_u_to_the_negative_one,
    _reduce_u_to_the_one_half,
    _reduce_power_with_constant_base,
    _reduce_power_of_power
]
