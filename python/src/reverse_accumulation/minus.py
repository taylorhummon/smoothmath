from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.reverse_accumulation.expression import Expression
    from src.reverse_accumulation.result import InternalResult
    from src.reverse_accumulation.custom_types import Real, VariableValues
from src.reverse_accumulation.expression import BinaryExpression

class Minus(BinaryExpression):
    def __init__(
        self: Minus,
        a: Expression,
        b: Expression
    ) -> None:
        super().__init__(a, b)

    def _evaluate(
        self: Minus,
        variableValues: VariableValues
    ) -> Real:
        aValue = self.a._evaluateUsingCache(variableValues)
        bValue = self.b._evaluateUsingCache(variableValues)
        return aValue - bValue

    def _derive(
        self: Minus,
        result: InternalResult,
        variableValues: VariableValues,
        seed: Real
    ) -> None:
        # d(a - b) = da - db
        self.a._derive(result, variableValues, seed)
        self.b._derive(result, variableValues, - seed)
