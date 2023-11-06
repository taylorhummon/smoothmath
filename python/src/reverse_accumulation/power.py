from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.reverse_accumulation.expression import Expression
    from src.reverse_accumulation.result import InternalResult
    from src.reverse_accumulation.custom_types import Real, VariableValues
import math
from src.reverse_accumulation.custom_exceptions import DomainException
from src.reverse_accumulation.expression import BinaryExpression

class Power(BinaryExpression):
    def __init__(
        self: Power,
        a: Expression,
        b: Expression
    ) -> None:
        super().__init__(a, b)

    # For a power a ** b, there are two over-arching cases we work with:
    # (I) the exponent, b, can be determined to be a constant integer
    #     e.g. a ** 2, a ** 3, or a ** (-1)
    # (II) otherwise
    #     e.g. e ** b, or 3 ** b, a ** b,
    # In case (I), we allow negative bases. In case (II), we only allow positive bases.

    def _evaluate(
        self: Power,
        variableValues: VariableValues
    ) -> Real:
        aValue = self.a._evaluateUsingCache(variableValues)
        bValue = self.b._evaluateUsingCache(variableValues)
        if self.b.lacksVariables and bValue.is_integer():
            if bValue >= 1:
                return aValue ** bValue
            elif bValue == 0:
                # Note: x ** 0 is smooth at x = 0 despite x ** y not being smooth at (0, 0)
                return 1
            else: # bValue <= -1
                self._ensureValueIsInDomainCaseI(aValue, bValue)
                return aValue ** bValue
        else: # bValue is not an integer
            self._ensureValueIsInDomainCaseII(aValue, bValue)
            return aValue ** bValue

    def _derive(
        self: Power,
        result: InternalResult,
        variableValues: VariableValues,
        seed: Real
    ) -> None:
        aValue = self.a._evaluateUsingCache(variableValues)
        bValue = self.b._evaluateUsingCache(variableValues)
        if self.b.lacksVariables and bValue.is_integer():
            if bValue >= 2:
                # d(a ** C) = C * a ** (C - 1) * da
                self.a._derive(result, variableValues, seed * bValue * (aValue ** (bValue - 1)))
            elif bValue == 1:
                # d(a ** 1) = da
                self.a._derive(result, variableValues, seed)
            elif bValue == 0:
                # Note: a ** 0 is smooth at a = 0 despite a ** b not being smooth at (0, 0)
                # d(a ** 0) = 0 * da
                self.a._derive(result, variableValues, 0)
            else: # bValue <= -1
                self._ensureValueIsInDomainCaseI(aValue, bValue)
                # d(a ** C) = C * a ** (C - 1) * da
                self.a._derive(result, variableValues, seed * bValue * (aValue ** (bValue - 1)))
        else: # bValue is not an integer
            self._ensureValueIsInDomainCaseII(aValue, bValue)
            selfValue = self._evaluateUsingCache(variableValues)
            # d(a ** b) = b * a ** (b - 1) * da + ln(a) * a ** b * db
            self.a._derive(result, variableValues, seed * bValue * selfValue / aValue)
            self.b._derive(result, variableValues, seed * math.log(aValue) * selfValue)

    def _ensureValueIsInDomainCaseI(
        self: Power,
        aValue: Real,
        bValue: Real
    ) -> None:
        if bValue <= -1 and aValue == 0:
            raise DomainException("Power(x, C) blows up around x = 0 when C is a negative integer")

    def _ensureValueIsInDomainCaseII(
        self: Power,
        aValue: Real,
        bValue: Real
    ) -> None:
        if aValue == 0:
            if bValue > 0:
                raise DomainException("Power(x, y) is not smooth around x = 0 for y > 0")
            elif bValue == 0:
                raise DomainException("Power(x, y) is not smooth around (x = 0, y = 0)")
            else: # bValue < 0
                raise DomainException("Power(x, y) blows up around x = 0 for y < 0")
        elif aValue < 0:
            raise DomainException("Power(x, y) is undefined for x < 0")
