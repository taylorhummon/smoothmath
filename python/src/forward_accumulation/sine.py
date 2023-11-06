from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.forward_accumulation.expression import Expression
    from src.forward_accumulation.variable import Variable
import math
from src.forward_accumulation.custom_types import VariableValues
from src.forward_accumulation.result import InternalResult
from src.forward_accumulation.expression import UnaryExpression

class Sine(UnaryExpression):
    def __init__(
        self: Sine,
        a: Expression
    ) -> None:
        super().__init__(a)

    def _derive(
        self: Sine,
        variableValues: VariableValues,
        withRespectTo: Variable
    ) -> InternalResult:
        aLacksVariables, aValue, aPartial = self.a._derive(variableValues, withRespectTo).toTriple()
        # d(sin(a)) = cos(a) * da
        return InternalResult(
            lacksVariables = aLacksVariables,
            value = math.sin(aValue),
            partial = math.cos(aValue) * aPartial
        )
