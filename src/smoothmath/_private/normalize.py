from __future__ import annotations
import logging
import smoothmath as sm
import smoothmath.expression as ex
import smoothmath._private.expression.base as base


def normalize_synthetic(
    expression: sm.Expression
) -> sm.Expression:
    fully_reduced = _fully_reduce_synthetic(expression)
    return _reintroduce_minus_and_divide(fully_reduced)


def _fully_reduce_synthetic(
    expression: sm.Expression
) -> sm.Expression:
    TOP = 1000
    for _ in range(0, TOP):
        if expression._is_fully_reduced:
            return expression
        expression = expression._take_reduction_step()
    logging.warning(f"Unable to fully reduce within {TOP} steps")
    expression._is_fully_reduced = True
    return expression


def _reintroduce_minus_and_divide(
    expression: sm.Expression
) -> sm.Expression:
    if isinstance(expression, base.NullaryExpression):
        return expression
    elif isinstance(expression, (base.UnaryExpression, base.ParameterizedUnaryExpression)):
        reassembled_inner = _reintroduce_minus_and_divide(expression._inner)
        return expression._rebuild(reassembled_inner)
    elif isinstance(expression, base.BinaryExpression):
        if isinstance(expression, ex.Plus) and isinstance(expression._right, ex.Negation):
            reassembled_left = _reintroduce_minus_and_divide(expression._left)
            reassembled_right = _reintroduce_minus_and_divide(expression._right._inner)
            return ex.Minus(reassembled_left, reassembled_right)
        elif isinstance(expression, ex.Multiply) and isinstance(expression._left, ex.Reciprocal):
            reassembled_numerator = _reintroduce_minus_and_divide(expression._right)
            reassembled_denominator = _reintroduce_minus_and_divide(expression._left._inner)
            return ex.Divide(reassembled_numerator, reassembled_denominator)
        else:
            reassembled_left = _reintroduce_minus_and_divide(expression._left)
            reassembled_right = _reintroduce_minus_and_divide(expression._right)
            return expression._rebuild(reassembled_left, reassembled_right)
    else:
        raise Exception("smoothmath internal error: unknown Expression base class")
