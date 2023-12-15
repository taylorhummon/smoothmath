from __future__ import annotations
import smoothmath as sm
import smoothmath.expression as ex
import smoothmath._private.expression.base as base
import smoothmath._private.reducers as r


def optimize_synthetic(
    expression: sm.Expression
) -> sm.Expression:
    disassembled = _disassemble_minus_and_divide(expression)
    reduced = _reduce_synthetic(disassembled)
    reassembled = _reassemble_minus_and_divide(reduced)
    return reassembled


def _reduce_synthetic(
    expression: sm.Expression
) -> sm.Expression:
    if isinstance(expression, base.NullaryExpression):
        return expression
    elif isinstance(expression, (base.UnaryExpression, base.ParameterizedUnaryExpression)):
        reduced_inner = _reduce_synthetic(expression._inner)
        rebuilt = expression._rebuild(reduced_inner)
        return r.apply_reducers(rebuilt)
    elif isinstance(expression, base.BinaryExpression):
        reduced_left = _reduce_synthetic(expression._left)
        reduced_right = _reduce_synthetic(expression._right)
        rebuilt = expression._rebuild(reduced_left, reduced_right)
        return r.apply_reducers(rebuilt)
    else:
        raise Exception("internal error: unknown expression kind")


def _disassemble_minus_and_divide(
    expression: sm.Expression
) -> sm.Expression:
    return expression # !!! to implement


def _reassemble_minus_and_divide(
    expression: sm.Expression
) -> sm.Expression:
    return expression # !!! to implement
