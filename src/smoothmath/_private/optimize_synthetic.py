from __future__ import annotations
import logging
import smoothmath as sm
import smoothmath.expression as ex
import smoothmath._private.expression.base as base
import smoothmath._private.reducers as r


def optimize_synthetic(
    expression: sm.Expression
) -> sm.Expression:
    disassembled = _disassemble_minus_and_divide(expression)
    reduced = _fully_reduce_synthetic(disassembled)
    reassembled = _reassemble_minus_and_divide(reduced)
    return reassembled


def _fully_reduce_synthetic(
    expression: sm.Expression
) -> sm.Expression:
    if expression._is_fully_reduced:
        return expression
    else:
        return _fully_reduce_synthetic(_next_expression(expression))


# # !!! this implementation will allow us to get out without crashing, but is worse for debugging
# def _fully_reduce_synthetic(
#     expression: sm.Expression
# ) -> sm.Expression:
#     TOP = 1000
#     for _ in range(0, TOP):
#         if expression._is_fully_reduced:
#             return expression
#         else:
#             expression = _next_expression(expression)
#     logging.warning(f"Unable to fully reduce within {TOP} steps")
#     expression._is_fully_reduced = True
#     return expression


def _next_expression(
    expression: sm.Expression
) -> sm.Expression:
    if isinstance(expression, (base.UnaryExpression, base.ParameterizedUnaryExpression)):
        if not expression._inner._is_fully_reduced:
            fully_reduced_inner = _fully_reduce_synthetic(expression._inner)
            return expression._rebuild(fully_reduced_inner)
        else: # inner expression is fully reduced
            return r.apply_reducer_or_mark_as_fully_reduced(expression)
    elif isinstance(expression, base.BinaryExpression):
        if not expression._left._is_fully_reduced:
            fully_reduced_left = _fully_reduce_synthetic(expression._left)
            return expression._rebuild(fully_reduced_left, expression._right)
        if not expression._right._is_fully_reduced:
            fully_reduced_right = _fully_reduce_synthetic(expression._right)
            return expression._rebuild(expression._left, fully_reduced_right)
        else: # both left and right inner expressions are reduced
            return r.apply_reducer_or_mark_as_fully_reduced(expression)
    else:
        raise Exception("smoothmath internal error: unknown Expression base class")


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
        raise Exception("smoothmath internal error: unknown Expression base class")


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
        raise Exception("smoothmath internal error: unknown Expression base class")


# !!! make use of something like the following
def _reassemble_minus(
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
        else:
            reassembled_left = _reassemble_minus_and_divide(expression._left)
            reassembled_right = _reassemble_minus_and_divide(expression._right)
            return expression._rebuild(reassembled_left, reassembled_right)
    else:
        raise Exception("smoothmath internal error: unknown Expression base class")
