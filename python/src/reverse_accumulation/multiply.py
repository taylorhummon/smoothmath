from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.reverse_accumulation.expression import Expression
    from src.reverse_accumulation.result import InternalResult
    from src.reverse_accumulation.custom_types import Real, VariableValues
from src.reverse_accumulation.expression import BinaryExpression

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
        aValue = self.a._evaluateUsingCache(variableValues)
        bValue = self.b._evaluateUsingCache(variableValues)
        return aValue * bValue

    def _derive(
        self: Multiply,
        result: InternalResult,
        variableValues: VariableValues,
        seed: Real
    ) -> None:
        aValue = self.a._evaluateUsingCache(variableValues)
        bValue = self.b._evaluateUsingCache(variableValues)
        # d(a * b) = b * da + a * db
        self.a._derive(result, variableValues, seed * bValue)
        self.b._derive(result, variableValues, seed * aValue)
