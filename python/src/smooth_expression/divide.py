from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.smooth_expression.custom_types import Real
    from src.smooth_expression.variable_values import VariableValues
    from src.smooth_expression.all_partials import AllPartials
    from src.smooth_expression.expression import Expression
from src.smooth_expression.custom_exceptions import DomainException
from src.smooth_expression.binary_expression import BinaryExpression

class Divide(BinaryExpression):
    def __init__(
        self: Divide,
        a: Expression,
        b: Expression
    ) -> None:
        super().__init__(a, b)

    def _evaluate(
        self: Divide,
        variableValues: VariableValues
    ) -> Real:
        if self._value is not None:
            return self._value
        aValue = self.a._evaluate(variableValues)
        bValue = self.b._evaluate(variableValues)
        # Note: 0 / b is smooth at b = 0 despite a / b not being smooth at (0, 0)
        if self.a.lacksVariables and aValue == 0:
            self._value = 0
        else:
            self._ensureValueIsInDomain(aValue, bValue)
            self._value = aValue / bValue
        return self._value

    def _computePartialAt(
        self: Divide,
        variableValues: VariableValues,
        withRespectTo: str
    ) -> tuple[bool, Real]:
        aValue = self.a._evaluate(variableValues)
        bValue = self.b._evaluate(variableValues)
        aLacksVariables, aPartial = self.a._computePartialAt(variableValues, withRespectTo)
        bLacksVariables, bPartial = self.b._computePartialAt(variableValues, withRespectTo)
        # Note: 0 / y is smooth at y = 0 despite x / y not being smooth at (0, 0)
        if aLacksVariables and aValue == 0:
            return (bLacksVariables, 0)
        else:
            self._ensureValueIsInDomain(aValue, bValue)
            # d(a / b) = (1 / b) * da - (a / b ** 2) * db
            return (
                aLacksVariables and bLacksVariables,
                (bValue * aPartial - aValue * bPartial) / bValue ** 2
            )

    def _computeAllPartialsAt(
        self: Divide,
        allPartials: AllPartials,
        variableValues: VariableValues,
        seed: Real
    ) -> None:
        aValue = self.a._evaluate(variableValues)
        bValue = self.b._evaluate(variableValues)
        # Note: 0 / b is smooth at b = 0 despite a / b not being smooth at (0, 0)
        if self.a.lacksVariables and aValue == 0:
            self.b._computeAllPartialsAt(allPartials, variableValues, 0)
        else:
            self._ensureValueIsInDomain(aValue, bValue)
            # d(a / b) = (1 / b) * da - (a / b ** 2) * db
            self.a._computeAllPartialsAt(allPartials, variableValues, seed / bValue)
            self.b._computeAllPartialsAt(allPartials, variableValues, - seed * aValue / (bValue ** 2))

    def _ensureValueIsInDomain(
        self: Divide,
        aValue: Real,
        bValue: Real
    ) -> None:
        if bValue == 0:
            if aValue == 0:
                raise DomainException("Divide(x, y) is not smooth around (x = 0, y = 0)")
            else: # aValue != 0
                raise DomainException("Divide(x, y) blows up around x != 0 and y = 0")
