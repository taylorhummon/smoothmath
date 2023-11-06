from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.forward_accumulation.expression import Expression
    from src.forward_accumulation.variable import Variable
from src.forward_accumulation.custom_types import VariableValues
from src.forward_accumulation.custom_exceptions import DomainException
from src.forward_accumulation.result import InternalResult
from src.forward_accumulation.expression import BinaryExpression

class Divide(BinaryExpression):
    def __init__(
        self: Divide,
        a: Expression,
        b: Expression
    ) -> None:
        super().__init__(a, b)

    def _derive(
        self: Divide,
        variableValues: VariableValues,
        withRespectTo: Variable
    ) -> InternalResult:
        aLacksVariables, aValue, aPartial = self.a._derive(variableValues, withRespectTo).toTriple()
        bLacksVariables, bValue, bPartial = self.b._derive(variableValues, withRespectTo).toTriple()
        # Note: 0 / y is smooth at y = 0 despite x / y not being smooth at (0, 0)
        if aLacksVariables and aValue == 0:
            return InternalResult(0, 0, bLacksVariables)
        if bValue == 0:
            if aValue == 0:
                raise DomainException("Divide(x, y) is not smooth around (x = 0, y = 0)")
            else: # aValue != 0
                raise DomainException("Divide(x, y) blows up around x != 0 and y = 0")
        # d(a / b) = (1 / b) * da - (a / b ** 2) * db
        return InternalResult(
            lacksVariables = aLacksVariables and bLacksVariables,
            value = aValue / bValue,
            partial = (bValue * aPartial - aValue * bPartial) / bValue ** 2
        )
