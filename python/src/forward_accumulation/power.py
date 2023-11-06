from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.forward_accumulation.expression import Expression
    from src.forward_accumulation.variable import Variable
import math
from src.forward_accumulation.custom_types import VariableValues
from src.forward_accumulation.custom_exceptions import DomainException
from src.forward_accumulation.single_result import InternalSingleResult
from src.forward_accumulation.expression import BinaryExpression

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

    def _derive(
        self: Power,
        variableValues: VariableValues,
        withRespectTo: Variable
    ) -> InternalSingleResult:
        aLacksVariables, aValue, aPartial = self.a._derive(variableValues, withRespectTo).toTriple()
        bLacksVariables, bValue, bPartial = self.b._derive(variableValues, withRespectTo).toTriple()
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
