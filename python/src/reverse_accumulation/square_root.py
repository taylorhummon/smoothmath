from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.reverse_accumulation.expression import Expression
    from src.reverse_accumulation.multi_result import InternalMultiResult
    from src.reverse_accumulation.custom_types import Real, VariableValues
import math
from src.reverse_accumulation.custom_exceptions import DomainException
from src.reverse_accumulation.expression import UnaryExpression

class SquareRoot(UnaryExpression):
    def __init__(
        self: SquareRoot,
        a: Expression
    ) -> None:
        super().__init__(a)

    def _evaluate(
        self: SquareRoot,
        variableValues: VariableValues
    ) -> Real:
        aValue = self.a._evaluateUsingCache(variableValues)
        self._ensureValueIsInDomain(aValue)
        return math.sqrt(aValue)

    def _derive(
        self: SquareRoot,
        multiResult: InternalMultiResult,
        variableValues: VariableValues,
        seed: Real
    ) -> None:
        aValue = self.a._evaluateUsingCache(variableValues)
        self._ensureValueIsInDomain(aValue)
        selfValue = self._evaluateUsingCache(variableValues)
        # d(sqrt(a)) = (1 / (2 sqrt(a))) * da
        self.a._derive(multiResult, variableValues, seed / (2 * selfValue))

    def _ensureValueIsInDomain(
        self: SquareRoot,
        aValue: Real
    ) -> None:
        if aValue == 0:
            raise DomainException("SquareRoot(x) is not smooth around x = 0")
        elif aValue < 0:
            raise DomainException("SquareRoot(x) is undefined for x < 0")
