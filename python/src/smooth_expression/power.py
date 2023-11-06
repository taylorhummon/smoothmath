from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.smooth_expression.custom_types import Real, VariableValues
    from src.smooth_expression.multi_result import InternalMultiResult
    from src.smooth_expression.expression import Expression
    from src.smooth_expression.variable import Variable
import math
from src.smooth_expression.custom_exceptions import DomainException
from src.smooth_expression.single_result import InternalSingleResult
from src.smooth_expression.binary_expression import BinaryExpression

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
        if self._value is not None:
            return self._value
        aValue = self.a._evaluate(variableValues)
        bValue = self.b._evaluate(variableValues)
        if self.b.lacksVariables and bValue.is_integer():
            if bValue >= 1:
                self._value = aValue ** bValue
            elif bValue == 0:
                # Note: x ** 0 is smooth at x = 0 despite x ** y not being smooth at (0, 0)
                self._value = 1
            else: # bValue <= -1
                self._ensureValueIsInDomainCaseI(aValue, bValue)
                self._value = aValue ** bValue
        else: # bValue is not an integer
            self._ensureValueIsInDomainCaseII(aValue, bValue)
            self._value = aValue ** bValue
        return self._value

    def _deriveSingle(
        self: Power,
        variableValues: VariableValues,
        withRespectTo: Variable
    ) -> InternalSingleResult:
        aLacksVariables, aValue, aPartial = self.a._deriveSingle(variableValues, withRespectTo).toTriple()
        bLacksVariables, bValue, bPartial = self.b._deriveSingle(variableValues, withRespectTo).toTriple()
        lacksVariables = aLacksVariables and bLacksVariables
        if bLacksVariables and bValue.is_integer(): # CASE I: has constant integer exponent
            if bValue >= 2:
                singleResultValue = aValue ** bValue
                # d(a ** C) = C * a ** (C - 1) * da
                singleResultPartial = bValue * (aValue ** (bValue - 1)) * aPartial
                return InternalSingleResult(lacksVariables, singleResultValue, singleResultPartial)
            elif bValue == 1:
                singleResultValue = aValue
                # d(a ** 1) = 1 * da
                singleResultPartial = aPartial
                return InternalSingleResult(lacksVariables, singleResultValue, singleResultPartial)
            elif bValue == 0:
                # Note: x ** 0 is smooth at x = 0 despite x ** y not being smooth at (0, 0)
                singleResultValue = 1
                # d(a ** 0) = 0 * da
                singleResultPartial = 0
                return InternalSingleResult(lacksVariables, singleResultValue, singleResultPartial)
            else: # bValue <= -1:
                if aValue == 0:
                    raise DomainException("Power(x, C) blows up around x = 0 when C is a negative integer")
                singleResultValue = aValue ** bValue
                # d(a ** C) = C * a ** (C - 1) * da
                singleResultPartial = (bValue * singleResultValue / aValue) * aPartial
                return InternalSingleResult(lacksVariables, singleResultValue, singleResultPartial)
        else: # CASE II: does not have a constant integer exponent
            if aValue > 0:
                singleResultValue = aValue ** bValue
                # d(a ** b) = b * a ** (b - 1) * da + ln(a) * a ** b * db
                singleResultPartial = (
                    (bValue * singleResultValue / aValue) * aPartial +
                    math.log(aValue) * singleResultValue * bPartial
                )
                return InternalSingleResult(lacksVariables, singleResultValue, singleResultPartial)
            elif aValue == 0:
                if bValue > 0:
                    raise DomainException("Power(x, y) is not smooth around x = 0 for y > 0")
                elif bValue == 0:
                    raise DomainException("Power(x, y) is not smooth around (x = 0, y = 0)")
                else: # bValue < 0
                    raise DomainException("Power(x, y) blows up around x = 0 for y < 0")
            else: # aValue < 0
                raise DomainException("Power(x, y) is undefined for x < 0")

    def _deriveMulti(
        self: Power,
        multiResult: InternalMultiResult,
        variableValues: VariableValues,
        seed: Real
    ) -> None:
        aValue = self.a._evaluate(variableValues)
        bValue = self.b._evaluate(variableValues)
        if self.b.lacksVariables and bValue.is_integer():
            if bValue >= 2:
                # d(a ** C) = C * a ** (C - 1) * da
                self.a._deriveMulti(multiResult, variableValues, seed * bValue * (aValue ** (bValue - 1)))
            elif bValue == 1:
                # d(a ** 1) = da
                self.a._deriveMulti(multiResult, variableValues, seed)
            elif bValue == 0:
                # Note: a ** 0 is smooth at a = 0 despite a ** b not being smooth at (0, 0)
                # d(a ** 0) = 0 * da
                self.a._deriveMulti(multiResult, variableValues, 0)
            else: # bValue <= -1
                self._ensureValueIsInDomainCaseI(aValue, bValue)
                # d(a ** C) = C * a ** (C - 1) * da
                self.a._deriveMulti(multiResult, variableValues, seed * bValue * (aValue ** (bValue - 1)))
        else: # bValue is not an integer
            self._ensureValueIsInDomainCaseII(aValue, bValue)
            selfValue = self._evaluate(variableValues)
            # d(a ** b) = b * a ** (b - 1) * da + ln(a) * a ** b * db
            self.a._deriveMulti(multiResult, variableValues, seed * bValue * selfValue / aValue)
            self.b._deriveMulti(multiResult, variableValues, seed * math.log(aValue) * selfValue)

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
