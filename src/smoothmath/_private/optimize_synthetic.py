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
        raise Exception("internal error: unknown Expression base class")


def _disassemble_minus_and_divide(
    expression: sm.Expression
) -> sm.Expression:
    if isinstance(expression, base.NullaryExpression):
        return expression
    elif isinstance(expression, (base.UnaryExpression, base.ParameterizedUnaryExpression)):
        disassembled_inner = _disassemble_minus_and_divide(expression._inner)
        return expression._rebuild(disassembled_inner)
    elif isinstance(expression, base.BinaryExpression):
        disassembled_left = _disassemble_minus_and_divide(expression._left)
        disassembled_right = _disassemble_minus_and_divide(expression._right)
        if isinstance(expression, ex.Minus):
            return ex.Plus(disassembled_left, ex.Negation(disassembled_right))
        elif isinstance(expression, ex.Divide):
            return ex.Multiply(ex.Reciprocal(disassembled_right), disassembled_left)
        else:
            return expression._rebuild(disassembled_left, disassembled_right)
    else:
        raise Exception("internal error: unknown Expression base class")


def _reassemble_minus_and_divide(
    expression: sm.Expression
) -> sm.Expression:
    if isinstance(expression, base.NullaryExpression):
        return expression
    elif isinstance(expression, (base.UnaryExpression, base.ParameterizedUnaryExpression)):
        reassembled_inner = _reassemble_minus_and_divide(expression._inner)
        return expression._rebuild(reassembled_inner)
    elif isinstance(expression, base.BinaryExpression):
        if isinstance(expression, ex.Plus) and isinstance(expression._right, ex.Negation):
            reassembled_left = _reassemble_minus_and_divide(expression._left)
            reassembled_right = _reassemble_minus_and_divide(expression._right._inner)
            return ex.Minus(reassembled_left, reassembled_right)
        elif isinstance(expression, ex.Multiply) and isinstance(expression._left, ex.Reciprocal):
            reassembled_numerator = _reassemble_minus_and_divide(expression._right)
            reassembled_denominator = _reassemble_minus_and_divide(expression._left._inner)
            return ex.Divide(reassembled_numerator, reassembled_denominator)
        else:
            reassembled_left = _reassemble_minus_and_divide(expression._left)
            reassembled_right = _reassemble_minus_and_divide(expression._right)
            return expression._rebuild(reassembled_left, reassembled_right)
    else:
        raise Exception("internal error: unknown Expression base class")
