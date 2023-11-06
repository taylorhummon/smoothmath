from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.forward_accumulation.expression import Expression
    from src.forward_accumulation.variable import Variable
import math
from src.forward_accumulation.custom_types import VariableValues
from src.forward_accumulation.custom_exceptions import DomainException
from src.forward_accumulation.single_result import InternalSingleResult
from src.forward_accumulation.expression import UnaryExpression

class SquareRoot(UnaryExpression):
    def __init__(
        self: SquareRoot,
        a: Expression
    ) -> None:
        super().__init__(a)

    def _derive(
        self: SquareRoot,
        variableValues: VariableValues,
        withRespectTo: Variable
    ) -> InternalSingleResult:
        aLacksVariables, aValue, aPartial = self.a._derive(variableValues, withRespectTo).toTriple()
        if aValue == 0:
            raise DomainException("SquareRoot(x) is not smooth around x = 0")
        elif aValue < 0:
            raise DomainException("SquareRoot(x) is undefined for x < 0")
        singleResultValue = math.sqrt(aValue)
        # d(sqrt(a)) = (1 / (2 sqrt(a))) * da
        return InternalSingleResult(
            lacksVariables = aLacksVariables,
            value = singleResultValue,
            partial = aPartial / (2 * singleResultValue)
        )
