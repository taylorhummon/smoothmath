from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.smooth_expression.custom_types import Real, VariableValues
    from src.smooth_expression.multi_result import InternalMultiResult
    from src.smooth_expression.expression import Expression
    from src.smooth_expression.variable import Variable
from src.smooth_expression.single_result import InternalSingleResult
from src.smooth_expression.binary_expression import BinaryExpression

class Multiply(BinaryExpression):
    def __init__(
        self: Multiply,
        a: Expression,
        b: Expression
    ) -> None:
        super().__init__(a, b)

    def _evaluate(
        self: Multiply,
        variableValues: VariableValues
    ) -> Real:
        if self._value is not None:
            return self._value
        aValue = self.a._evaluate(variableValues)
        bValue = self.b._evaluate(variableValues)
        self._value = aValue * bValue
        return self._value

    def _deriveSingle(
        self: Multiply,
        variableValues: VariableValues,
        withRespectTo: Variable
    ) -> InternalSingleResult:
        aLacksVariables, aValue, aPartial = self.a._deriveSingle(variableValues, withRespectTo).toTriple()
        bLacksVariables, bValue, bPartial = self.b._deriveSingle(variableValues, withRespectTo).toTriple()
        # d(a * b) = b * da + a * db
        return InternalSingleResult(
            lacksVariables = aLacksVariables and bLacksVariables,
            value = aValue * bValue,
            partial = bValue * aPartial + aValue * bPartial
        )

    def _deriveMulti(
        self: Multiply,
        multiResult: InternalMultiResult,
        variableValues: VariableValues,
        seed: Real
    ) -> None:
        aValue = self.a._evaluate(variableValues)
        bValue = self.b._evaluate(variableValues)
        # d(a * b) = b * da + a * db
        self.a._deriveMulti(multiResult, variableValues, seed * bValue)
        self.b._deriveMulti(multiResult, variableValues, seed * aValue)
