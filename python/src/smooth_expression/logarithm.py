from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.smooth_expression.custom_types import Real, VariableValues
    from src.smooth_expression.multi_result import InternalMultiResult
    from src.smooth_expression.expression import Expression
    from src.smooth_expression.variable import Variable
import math
from src.smooth_expression.custom_exceptions import DomainException
from src.smooth_expression.unary_expression import UnaryExpression

class Logarithm(UnaryExpression):
    def __init__(
        self: Logarithm,
        a: Expression,
        base: Real = math.e
    ) -> None:
        super().__init__(a)
        if base <= 0:
            raise Exception("Logarithms must have a positive base")
        elif base == 1:
            raise Exception("Logarithms cannot have base = 1")
        self._base : Real
        self._base = base

    def _evaluate(
        self: Logarithm,
        variableValues: VariableValues
    ) -> Real:
        if self._value is not None:
            return self._value
        aValue = self.a._evaluate(variableValues)
        self._ensureValueIsInDomain(aValue)
        self._value = math.log(aValue, self._base)
        return self._value

    def _deriveSingle(
        self: Logarithm,
        variableValues: VariableValues,
        withRespectTo: Variable
    ) -> tuple[bool, Real]:
        aValue = self.a._evaluate(variableValues)
        aLacksVariables, aPartial = self.a._deriveSingle(variableValues, withRespectTo)
        if aValue == 0:
            raise DomainException("Logarithm(x) blows up around x = 0")
        elif aValue < 0:
            raise DomainException("Logarithm(x) is undefined for x < 0")
        # d(log_C(a)) = (1 / (ln(C) * a)) * da
        return (
            aLacksVariables,
            aPartial / (math.log(self._base) * aValue)
        )

    def _deriveMulti(
        self: Logarithm,
        multiResult: InternalMultiResult,
        variableValues: VariableValues,
        seed: Real
    ) -> None:
        aValue = self.a._evaluate(variableValues)
        self._ensureValueIsInDomain(aValue)
        # d(log_C(a)) = (1 / (ln(C) * a)) * da
        self.a._deriveMulti(multiResult, variableValues, seed / (math.log(self._base) * aValue))

    def _ensureValueIsInDomain(
        self: Logarithm,
        aValue: Real
    ) -> None:
        if aValue == 0:
            raise DomainException("Logarithm(x) blows up around x = 0")
        elif aValue < 0:
            raise DomainException("Logarithm(x) is undefined for x < 0")

    def __str__(
        self: Logarithm
    ) -> str:
        if self._base == math.e:
            return f"Logarithm({self.a})"
        else:
            return f"Logarithm({self.a}, base = {self._base})"
