from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.forward_accumulation.expression import Expression
    from src.forward_accumulation.variable import Variable
import math
from src.forward_accumulation.custom_types import VariableValues
from src.forward_accumulation.single_result import InternalSingleResult
from src.forward_accumulation.expression import UnaryExpression

class Cosine(UnaryExpression):
    def __init__(
        self: Cosine,
        a: Expression
    ) -> None:
        super().__init__(a)

    def _derive(
        self: Cosine,
        variableValues: VariableValues,
        withRespectTo: Variable
    ) -> InternalSingleResult:
        aLacksVariables, aValue, aPartial = self.a._derive(variableValues, withRespectTo).toTriple()
        # d(cos(a)) = - sin(a) * da
        return InternalSingleResult(
            lacksVariables = aLacksVariables,
            value = math.cos(aValue),
            partial = - math.sin(aValue) * aPartial
        )
