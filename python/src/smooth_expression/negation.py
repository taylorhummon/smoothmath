from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.smooth_expression.custom_types import Real
    from src.smooth_expression.variable_values import VariableValues
    from src.smooth_expression.all_partials import AllPartials
    from src.smooth_expression.expression import Expression
from src.smooth_expression.unary_expression import UnaryExpression

class Negation(UnaryExpression):
    def __init__(
        self: Negation,
        a: Expression
    ) -> None:
        super().__init__(a)

    def _evaluate(
        self: Negation,
        variableValues: VariableValues
    ) -> Real:
        if self._value is not None:
            return self._value
        aValue = self.a._evaluate(variableValues)
        self._value = - aValue
        return self._value

    def _partialAt(
        self: Negation,
        variableValues: VariableValues,
        withRespectTo: str
    ) -> tuple[bool, Real]:
        aLacksVariables, aPartial = self.a._partialAt(variableValues, withRespectTo)
        # d(-a) = -da
        return (
            aLacksVariables,
            - aPartial
        )

    def _allPartialsAt(
        self: Negation,
        allPartials: AllPartials,
        variableValues: VariableValues,
        seed: Real
    ) -> None:
        # d(-a) = -da
        self.a._allPartialsAt(allPartials, variableValues, - seed)
