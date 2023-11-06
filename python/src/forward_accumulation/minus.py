from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.forward_accumulation.expression import Expression
    from src.forward_accumulation.variable import Variable
from src.forward_accumulation.custom_types import VariableValues
from src.forward_accumulation.result import InternalResult
from src.forward_accumulation.expression import BinaryExpression

class Minus(BinaryExpression):
    def __init__(
        self: Minus,
        a: Expression,
        b: Expression
    ) -> None:
        super().__init__(a, b)

    def _derive(
        self: Minus,
        variableValues: VariableValues,
        withRespectTo: Variable
    ) -> InternalResult:
        aLacksVariables, aValue, aPartial = self.a._derive(variableValues, withRespectTo).toTriple()
        bLacksVariables, bValue, bPartial = self.b._derive(variableValues, withRespectTo).toTriple()
        # d(a - b) = da - db
        return InternalResult(
            lacksVariables = aLacksVariables and bLacksVariables,
            value = aValue - bValue,
            partial = aPartial - bPartial
        )
