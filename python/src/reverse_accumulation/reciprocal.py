from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.reverse_accumulation.expression import Expression
    from src.reverse_accumulation.multi_result import InternalMultiResult
    from src.reverse_accumulation.custom_types import Real, VariableValues
from src.reverse_accumulation.custom_exceptions import DomainException
from src.reverse_accumulation.expression import UnaryExpression

class Reciprocal(UnaryExpression):
    def __init__(
        self: Reciprocal,
        a: Expression
    ) -> None:
        super().__init__(a)

    def _evaluate(
        self: Reciprocal,
        variableValues: VariableValues
    ) -> Real:
        aValue = self.a._evaluateUsingCache(variableValues)
        self._ensureValueIsInDomain(aValue)
        return 1 / aValue

    def _derive(
        self: Reciprocal,
        multiResult: InternalMultiResult,
        variableValues: VariableValues,
        seed: Real
    ) -> None:
        aValue = self.a._evaluateUsingCache(variableValues)
        self._ensureValueIsInDomain(aValue)
        selfValue = self._evaluateUsingCache(variableValues)
        # d(1 / a) = - (1 / a ** 2) * da
        self.a._derive(multiResult, variableValues, - seed * (selfValue ** 2))

    def _ensureValueIsInDomain(
        self: Reciprocal,
        aValue: Real
    ) -> None:
        if aValue == 0:
            raise DomainException("Reciprocal(x) blows up around x = 0")
