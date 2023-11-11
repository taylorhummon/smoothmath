from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.smooth_expression.custom_types import Real
    from src.smooth_expression.variable_values import VariableValues
    from src.smooth_expression.all_partials import AllPartials
    from src.smooth_expression.expression import Expression
from src.smooth_expression.custom_exceptions import DomainException
from src.smooth_expression.unary_expression import UnaryExpression

class Reciprocal(UnaryExpression):
    def __init__(
        self: Reciprocal,
        a: Expression
    ) -> None:
        super().__init__(a)

    def _evaluate(
        self: Reciprocal,
        variableValues: VariableValues
    ) -> Real:
        if self._value is not None:
            return self._value
        aValue = self.a._evaluate(variableValues)
        self._ensureValueIsInDomain(aValue)
        self._value = 1 / aValue
        return self._value

    def _computePartialAt(
        self: Reciprocal,
        variableValues: VariableValues,
        withRespectTo: str
    ) -> tuple[bool, Real]:
        aValue = self.a._evaluate(variableValues)
        aLacksVariables, aPartial = self.a._computePartialAt(variableValues, withRespectTo)
        self._ensureValueIsInDomain(aValue)
        resultValue = self._evaluate(variableValues)
        # d(1 / a) = - (1 / a ** 2) * da
        return (
            aLacksVariables,
            - (resultValue ** 2) * aPartial
        )

    def _computeAllPartialsAt(
        self: Reciprocal,
        allPartials: AllPartials,
        variableValues: VariableValues,
        seed: Real
    ) -> None:
        aValue = self.a._evaluate(variableValues)
        self._ensureValueIsInDomain(aValue)
        selfValue = self._evaluate(variableValues)
        # d(1 / a) = - (1 / a ** 2) * da
        self.a._computeAllPartialsAt(allPartials, variableValues, - seed * (selfValue ** 2))

    def _ensureValueIsInDomain(
        self: Reciprocal,
        aValue: Real
    ) -> None:
        if aValue == 0:
            raise DomainException("Reciprocal(x) blows up around x = 0")
