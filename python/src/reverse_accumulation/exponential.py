from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.reverse_accumulation.expression import Expression
    from src.reverse_accumulation.multi_result import InternalMultiResult
    from src.reverse_accumulation.custom_types import Real, VariableValues
import math
from src.reverse_accumulation.expression import UnaryExpression

class Exponential(UnaryExpression):
    def __init__(
        self: Exponential,
        exponent: Expression,
        base: Real = math.e
    ) -> None:
        super().__init__(exponent)
        if base <= 0:
            raise Exception("Exponentials must have a positive base")
        self.base: Real
        self.base = base

    def _evaluate(
        self: Exponential,
        variableValues: VariableValues
    ) -> Real:
        aValue = self.a._evaluateUsingCache(variableValues)
        return self.base ** aValue

    def _derive(
        self: Exponential,
        multiResult: InternalMultiResult,
        variableValues: VariableValues,
        seed: Real
    ) -> None:
        selfValue = self._evaluateUsingCache(variableValues)
        # d(e ** a) = e ** a * da
        self.a._derive(multiResult, variableValues, seed * math.log(self.base) * selfValue)
