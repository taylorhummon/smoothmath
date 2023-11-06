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

class Cosine(UnaryExpression):
    def __init__(
        self: Cosine,
        a: Expression
    ) -> None:
        super().__init__(a)

    def _evaluate(
        self: Cosine,
        variableValues: VariableValues
    ) -> Real:
        if self._value is not None:
            return self._value
        aValue = self.a._evaluate(variableValues)
        self._value = math.cos(aValue)
        return self._value

    def _deriveSingle(
        self: Cosine,
        variableValues: VariableValues,
        withRespectTo: Variable
    ) -> InternalSingleResult:
        aLacksVariables, aValue, aPartial = self.a._deriveSingle(variableValues, withRespectTo).toTriple()
        # d(cos(a)) = - sin(a) * da
        return InternalSingleResult(
            lacksVariables = aLacksVariables,
            value = math.cos(aValue),
            partial = - math.sin(aValue) * aPartial
        )

    def _deriveMulti(
        self: Cosine,
        multiResult: InternalMultiResult,
        variableValues: VariableValues,
        seed: Real
    ) -> None:
        aValue = self.a._evaluate(variableValues)
        # d(cos(a)) = - sin(a) * da
        self.a._deriveMulti(multiResult, variableValues, - seed * math.sin(aValue))
