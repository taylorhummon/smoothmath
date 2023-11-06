from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.forward_accumulation.expression import Expression
    from src.forward_accumulation.variable import Variable
from src.forward_accumulation.custom_types import VariableValues
from src.forward_accumulation.custom_exceptions import DomainException
from src.forward_accumulation.single_result import InternalSingleResult
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
    ) -> InternalSingleResult:
        aLacksVariables, aValue, aPartial = self.a._derive(variableValues, withRespectTo).toTriple()
        if aValue == 0:
            raise DomainException("Reciprocal(x) blows up around x = 0")
        singleResultValue = 1 / aValue
        # d(1 / a) = - (1 / a ** 2) * da
        return InternalSingleResult(
            lacksVariables = aLacksVariables,
            value = singleResultValue,
            partial = - (singleResultValue ** 2) * aPartial
        )
