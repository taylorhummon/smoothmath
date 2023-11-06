from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.reverse_accumulation.expression import Expression
    from src.reverse_accumulation.multi_result import InternalMultiResult
    from src.reverse_accumulation.custom_types import Real, VariableValues
import math
from src.reverse_accumulation.custom_exceptions import DomainException
from src.reverse_accumulation.expression import UnaryExpression

class Logarithm(UnaryExpression):
    def __init__(
        self: Logarithm,
        a: Expression,
        base: Real = math.e
    ) -> None:
        super().__init__(a)
        if base <= 0:
            raise Exception("Logarithms must have a positive base")
        elif base == 1:
            raise Exception("Logarithms cannot have base = 1")
        base: Real
        self.base = base

    def _evaluate(
        self: Logarithm,
        variableValues: VariableValues
    ) -> Real:
        aValue = self.a._evaluateUsingCache(variableValues)
        self._ensureValueIsInDomain(aValue)
        return math.log(aValue, self.base)

    def _derive(
        self: Logarithm,
        multiResult: InternalMultiResult,
        variableValues: VariableValues,
        seed: Real
    ) -> None:
        aValue = self.a._evaluateUsingCache(variableValues)
        self._ensureValueIsInDomain(aValue)
        # d(log_C(a)) = (1 / (ln(C) * a)) * da
        self.a._derive(multiResult, variableValues, seed / (math.log(self.base) * aValue))

    def _ensureValueIsInDomain(
        self: Logarithm,
        aValue: Real
    ) -> None:
        if aValue == 0:
            raise DomainException("Logarithm(x) blows up around x = 0")
        elif aValue < 0:
            raise DomainException("Logarithm(x) is undefined for x < 0")
