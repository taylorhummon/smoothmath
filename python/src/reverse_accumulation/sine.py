from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.reverse_accumulation.expression import Expression
    from src.reverse_accumulation.multi_result import InternalMultiResult
    from src.reverse_accumulation.custom_types import Real, VariableValues
import math
from src.reverse_accumulation.expression import UnaryExpression

class Sine(UnaryExpression):
    def __init__(
        self: Sine,
        a: Expression
    ) -> None:
        super().__init__(a)

    def _evaluate(
        self: Sine,
        variableValues: VariableValues
    ) -> Real:
        aValue = self.a._evaluateUsingCache(variableValues)
        return math.sin(aValue)

    def _derive(
        self: Sine,
        multiResult: InternalMultiResult,
        variableValues: VariableValues,
        seed: Real
    ) -> None:
        aValue = self.a._evaluateUsingCache(variableValues)
        # d(sin(a)) = cos(a) * da
        self.a._derive(multiResult, variableValues, seed * math.cos(aValue))
