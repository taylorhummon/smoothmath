from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.smooth_expression.custom_types import Real, VariableValues
    from src.smooth_expression.multi_result import InternalMultiResult
    from src.smooth_expression.expression import Expression
    from src.smooth_expression.variable import Variable
from src.smooth_expression.custom_exceptions import DomainException
from src.smooth_expression.single_result import InternalSingleResult
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

    def _deriveSingle(
        self: Divide,
        variableValues: VariableValues,
        withRespectTo: Variable
    ) -> InternalSingleResult:
        aLacksVariables, aValue, aPartial = self.a._deriveSingle(variableValues, withRespectTo).toTriple()
        bLacksVariables, bValue, bPartial = self.b._deriveSingle(variableValues, withRespectTo).toTriple()
        # Note: 0 / y is smooth at y = 0 despite x / y not being smooth at (0, 0)
        if aLacksVariables and aValue == 0:
            return InternalSingleResult(0, 0, bLacksVariables)
        if bValue == 0:
            if aValue == 0:
                raise DomainException("Divide(x, y) is not smooth around (x = 0, y = 0)")
            else: # aValue != 0
                raise DomainException("Divide(x, y) blows up around x != 0 and y = 0")
        # d(a / b) = (1 / b) * da - (a / b ** 2) * db
        return InternalSingleResult(
            lacksVariables = aLacksVariables and bLacksVariables,
            value = aValue / bValue,
            partial = (bValue * aPartial - aValue * bPartial) / bValue ** 2
        )

    def _deriveMulti(
        self: Divide,
        multiResult: InternalMultiResult,
        variableValues: VariableValues,
        seed: Real
    ) -> None:
        aValue = self.a._evaluate(variableValues)
        bValue = self.b._evaluate(variableValues)
        # Note: 0 / b is smooth at b = 0 despite a / b not being smooth at (0, 0)
        if self.a.lacksVariables and aValue == 0:
            self.b._deriveMulti(multiResult, variableValues, 0)
        else:
            self._ensureValueIsInDomain(aValue, bValue)
            # d(a / b) = (1 / b) * da - (a / b ** 2) * dv
            self.a._deriveMulti(multiResult, variableValues, seed / bValue)
            self.b._deriveMulti(multiResult, variableValues, - seed * aValue / (bValue ** 2))

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
