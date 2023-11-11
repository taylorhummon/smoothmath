from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.smooth_expression.custom_types import Real
    from src.smooth_expression.variable_values import VariableValues
    from src.smooth_expression.all_partials import AllPartials
    from src.smooth_expression.expression import Expression
import math
from src.smooth_expression.unary_expression import UnaryExpression

class Exponential(UnaryExpression):
    def __init__(
        self: Exponential,
        exponent: Expression,
        base: Real = math.e
    ) -> None:
        super().__init__(exponent)
        if base <= 0:
            raise Exception("Exponentials must have a positive base")
        self._base : Real
        self._base = base

    def _evaluate(
        self: Exponential,
        variableValues: VariableValues
    ) -> Real:
        if self._value is not None:
            return self._value
        aValue = self.a._evaluate(variableValues)
        self._value = self._base ** aValue
        return self._value

    def _computePartialAt(
        self: Exponential,
        variableValues: VariableValues,
        withRespectTo: str
    ) -> tuple[bool, Real]:
        aValue = self.a._evaluate(variableValues)
        aLacksVariables, aPartial = self.a._computePartialAt(variableValues, withRespectTo)
        resultValue = self._base ** aValue
        # d(C ** a) = ln(C) * C ** a * da
        return (
            aLacksVariables,
            math.log(self._base) * resultValue * aPartial
        )

    def _computeAllPartialsAt(
        self: Exponential,
        allPartials: AllPartials,
        variableValues: VariableValues,
        seed: Real
    ) -> None:
        selfValue = self._evaluate(variableValues)
        # d(e ** a) = e ** a * da
        self.a._computeAllPartialsAt(allPartials, variableValues, seed * math.log(self._base) * selfValue)


    def __str__(
        self: Exponential
    ) -> str:
        if self._base == math.e:
            return f"Exponential({self.a})"
        else:
            return f"Exponential({self.a}, base = {self._base})"
