from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.smooth_expression.custom_types import Real
    from src.smooth_expression.variable_values import VariableValues
    from src.smooth_expression.all_partials import AllPartials
    from src.smooth_expression.expression import Expression
import math
from src.smooth_expression.custom_exceptions import DomainException
from src.smooth_expression.binary_expression import BinaryExpression

# For a power a ** b, there are two over-arching cases we work with:
# (I) the exponent, b, can be determined to be a constant integer
#     e.g. a ** 2, a ** 3, or a ** (-1)
# (II) otherwise
#     e.g. e ** b, or 3 ** b, a ** b,
# In case (I), we allow negative bases. In case (II), we only allow positive bases.

def _isCaseI(
        bValue: Real,
        bLacksVariables: bool
    ) -> bool:
        return bLacksVariables and bValue.is_integer()

class Power(BinaryExpression):
    def __init__(
        self: Power,
        a: Expression,
        b: Expression
    ) -> None:
        super().__init__(a, b)

    def _evaluate(
        self: Power,
        variableValues: VariableValues
    ) -> Real:
        if self._value is not None:
            return self._value
        aValue = self.a._evaluate(variableValues)
        bValue = self.b._evaluate(variableValues)
        if _isCaseI(bValue, self.b.lacksVariables):
            self._ensureValueIsInDomainCaseI(aValue, bValue)
        else: # Case II
            self._ensureValueIsInDomainCaseII(aValue, bValue)
        self._value = aValue ** bValue
        return self._value

    def _computePartialAt(
        self: Power,
        variableValues: VariableValues,
        withRespectTo: str
    ) -> tuple[bool, Real]:
        aValue = self.a._evaluate(variableValues)
        bValue = self.b._evaluate(variableValues)
        aLacksVariables, aPartial = self.a._computePartialAt(variableValues, withRespectTo)
        bLacksVariables, bPartial = self.b._computePartialAt(variableValues, withRespectTo)
        resultLacksVariables = aLacksVariables and bLacksVariables
        if _isCaseI(bValue, self.b.lacksVariables):
            self._ensureValueIsInDomainCaseI(aValue, bValue)
            resultPartial = self._partialCaseI(aValue, aPartial, bValue)
            return (resultLacksVariables, resultPartial)
        else: # Case II
            self._ensureValueIsInDomainCaseII(aValue, bValue)
            resultPartial = self._partialCaseII(aValue, aPartial, bValue, bPartial)
            return (resultLacksVariables, resultPartial)

    def _partialCaseI(
        self: Power,
        aValue: Real,
        aPartial: Real,
        bValue: Real
    ) -> Real:
        if bValue == 0:
            # Note: x ** 0 is smooth at x = 0 despite x ** y not being smooth at (0, 0)
            # d(a ** 0) = 0 * da
            return 0
        elif bValue == 1:
            # d(a ** 1) = 1 * da
            return aPartial
        else: # bValue >= 2 or bValue <= -1
            # d(a ** C) = C * a ** (C - 1) * da
            return bValue * (aValue ** (bValue - 1)) * aPartial

    def _partialCaseII(
        self,
        aValue: Real,
        aPartial: Real,
        bValue: Real,
        bPartial: Real
    ) -> Real:
        # d(a ** b) = b * a ** (b - 1) * da + ln(a) * a ** b * db
        return (
            bValue * (aValue ** (bValue - 1)) * aPartial +
            math.log(aValue) * (aValue ** bValue) * bPartial
        )

    def _computeAllPartialsAt(
        self: Power,
        allPartials: AllPartials,
        variableValues: VariableValues,
        seed: Real
    ) -> None:
        aValue = self.a._evaluate(variableValues)
        bValue = self.b._evaluate(variableValues)
        if _isCaseI(bValue, self.b.lacksVariables):
            self._ensureValueIsInDomainCaseI(aValue, bValue)
            nextSeed = self._nextSeedCaseI(aValue, bValue, seed)
            self.a._computeAllPartialsAt(allPartials, variableValues, nextSeed)
        else: # Case II
            self._ensureValueIsInDomainCaseII(aValue, bValue)
            # d(a ** b) = b * a ** (b - 1) * da + ln(a) * a ** b * db
            nextSeedA = self._nextSeedACaseII(aValue, bValue, seed)
            nextSeedB = self._nextSeedBCaseII(aValue, bValue, seed)
            self.a._computeAllPartialsAt(allPartials, variableValues, nextSeedA)
            self.b._computeAllPartialsAt(allPartials, variableValues, nextSeedB)

    def _nextSeedCaseI(
        self: Power,
        aValue: Real,
        bValue: Real,
        seed: Real
    ) -> Real:
        if bValue == 0:
            # Note: a ** 0 is smooth at a = 0 despite a ** b not being smooth at (0, 0)
            # d(a ** 0) = 0 * da
            return 0
        elif bValue == 1:
            # d(a ** 1) = da
            return seed
        else: # bValue >= 2 or bValue <= -1
            # d(a ** C) = C * a ** (C - 1) * da
            return seed * bValue * (aValue ** (bValue - 1))

    def _nextSeedACaseII(
        self: Power,
        aValue: Real,
        bValue: Real,
        seed: Real
    ) -> Real:
        return seed * bValue * aValue ** (bValue - 1)

    def _nextSeedBCaseII(
        self: Power,
        aValue: Real,
        bValue: Real,
        seed: Real
    ) -> Real:
        return seed * math.log(aValue) * aValue ** bValue

    def _ensureValueIsInDomainCaseI(
        self: Power,
        aValue: Real,
        bValue: Real
    ) -> None:
        if aValue == 0 and bValue <= -1:
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
