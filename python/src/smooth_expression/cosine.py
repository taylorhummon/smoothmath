from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.smooth_expression.custom_types import Real
    from src.smooth_expression.variable_values import VariableValues
    from src.smooth_expression.all_partials import AllPartials
    from src.smooth_expression.expression import Expression
import math
from src.smooth_expression.unary_expression import UnaryExpression

class Cosine(UnaryExpression):
    def __init__(
        self: Cosine,
        a: Expression
    ) -> None:
        super().__init__(a)

    def _evaluate(
        self: Cosine,
        variableValues: VariableValues
    ) -> Real:
        if self._value is not None:
            return self._value
        aValue = self.a._evaluate(variableValues)
        self._value = math.cos(aValue)
        return self._value

    def _partialAt(
        self: Cosine,
        variableValues: VariableValues,
        withRespectTo: str
    ) -> tuple[bool, Real]:
        aValue = self.a._evaluate(variableValues)
        aLacksVariables, aPartial = self.a._partialAt(variableValues, withRespectTo)
        # d(cos(a)) = - sin(a) * da
        return (
             aLacksVariables,
            - math.sin(aValue) * aPartial
        )

    def _allPartialsAt(
        self: Cosine,
        allPartials: AllPartials,
        variableValues: VariableValues,
        seed: Real
    ) -> None:
        aValue = self.a._evaluate(variableValues)
        # d(cos(a)) = - sin(a) * da
        self.a._allPartialsAt(allPartials, variableValues, - seed * math.sin(aValue))
