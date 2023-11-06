from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.smooth_expression.custom_types import Real, VariableValues
    from src.smooth_expression.multi_result import InternalMultiResult
    from src.smooth_expression.expression import Expression
    from src.smooth_expression.variable import Variable
import math
from src.smooth_expression.single_result import InternalSingleResult
from src.smooth_expression.unary_expression import UnaryExpression

class Exponential(UnaryExpression):
    def __init__(
        self: Exponential,
        exponent: Expression,
        base: Real = math.e
    ) -> None:
        super().__init__(exponent)
        if base <= 0:
            raise Exception("Exponentials must have a positive base")
        self._base : Real
        self._base = base

    def _evaluate(
        self: Exponential,
        variableValues: VariableValues
    ) -> Real:
        if self._value is not None:
            return self._value
        aValue = self.a._evaluate(variableValues)
        self._value = self._base ** aValue
        return self._value

    def _deriveSingle(
        self: Exponential,
        variableValues: VariableValues,
        withRespectTo: Variable
    ) -> InternalSingleResult:
        aLacksVariables, aValue, aPartial = self.a._deriveSingle(variableValues, withRespectTo).toTriple()
        singleResultValue = self._base ** aValue
        # d(C ** b) = ln(C) * C ** b * db
        return InternalSingleResult(
            lacksVariables = aLacksVariables,
            value = singleResultValue,
            partial = math.log(self._base) * singleResultValue * aPartial
        )

    def _deriveMulti(
        self: Exponential,
        multiResult: InternalMultiResult,
        variableValues: VariableValues,
        seed: Real
    ) -> None:
        selfValue = self._evaluate(variableValues)
        # d(e ** a) = e ** a * da
        self.a._deriveMulti(multiResult, variableValues, seed * math.log(self._base) * selfValue)


    def __str__(
        self: Exponential
    ) -> str:
        if self._base == math.e:
            return f"Exponential({self.a})"
        else:
            return f"Exponential({self.a}, base = {self._base})"
