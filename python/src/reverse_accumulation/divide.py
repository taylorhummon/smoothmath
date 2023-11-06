from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.reverse_accumulation.expression import Expression
    from src.reverse_accumulation.result import InternalResult
    from src.reverse_accumulation.custom_types import Real, VariableValues
from src.reverse_accumulation.custom_exceptions import DomainException
from src.reverse_accumulation.expression import BinaryExpression

class Divide(BinaryExpression):
    def __init__(
        self: Divide,
        a: Expression,
        b: Expression
    ) -> None:
        super().__init__(a, b)

    def _evaluate(
        self: Divide,
        variableValues: VariableValues
    ) -> Real:
        aValue = self.a._evaluateUsingCache(variableValues)
        bValue = self.b._evaluateUsingCache(variableValues)
        # Note: 0 / b is smooth at b = 0 despite a / b not being smooth at (0, 0)
        if self.a.lacksVariables and aValue == 0:
            return 0
        else:
            self._ensureValueIsInDomain(aValue, bValue)
            return aValue / bValue

    def _derive(
        self: Divide,
        result: InternalResult,
        variableValues: VariableValues,
        seed: Real
    ) -> None:
        aValue = self.a._evaluateUsingCache(variableValues)
        bValue = self.b._evaluateUsingCache(variableValues)
        # Note: 0 / b is smooth at b = 0 despite a / b not being smooth at (0, 0)
        if self.a.lacksVariables and aValue == 0:
            self.b._derive(result, variableValues, 0)
        else:
            self._ensureValueIsInDomain(aValue, bValue)
            # d(a / b) = (1 / b) * da - (a / b ** 2) * dv
            self.a._derive(result, variableValues, seed / bValue)
            self.b._derive(result, variableValues, - seed * aValue / (bValue ** 2))

    def _ensureValueIsInDomain(
        self: Divide,
        aValue: Real,
        bValue: Real
    ) -> None:
        if bValue == 0:
            if aValue == 0:
                raise DomainException("Divide(x, y) is not smooth around (x = 0, y = 0)")
            else: # aValue != 0
                raise DomainException("Divide(x, y) blows up around x != 0 and y = 0")
