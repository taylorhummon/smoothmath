from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.forward_accumulation.expression import Expression
    from src.forward_accumulation.variable import Variable
from src.forward_accumulation.custom_types import VariableValues
from src.forward_accumulation.custom_exceptions import DomainException
from src.forward_accumulation.result import InternalResult
from src.forward_accumulation.expression import UnaryExpression

class Reciprocal(UnaryExpression):
    def __init__(
        self: Reciprocal,
        a: Expression
    ) -> None:
        super().__init__(a)

    def _derive(
        self: Reciprocal,
        variableValues: VariableValues,
        withRespectTo: Variable
    ) -> InternalResult:
        aLacksVariables, aValue, aPartial = self.a._derive(variableValues, withRespectTo).toTriple()
        if aValue == 0:
            raise DomainException("Reciprocal(x) blows up around x = 0")
        resultValue = 1 / aValue
        # d(1 / a) = - (1 / a ** 2) * da
        return InternalResult(
            lacksVariables = aLacksVariables,
            value = resultValue,
            partial = - (resultValue ** 2) * aPartial
        )
