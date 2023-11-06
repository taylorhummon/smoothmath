from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.smooth_expression.custom_types import Real, VariableValues
    from src.smooth_expression.variable import Variable
from abc import ABC, abstractmethod
from src.smooth_expression.single_result import SingleResult, InternalSingleResult
from src.smooth_expression.multi_result import MultiResult, InternalMultiResult

class Expression(ABC):
    def __init__(
        self: Expression,
        lacksVariables: bool
    ) -> None:
        self.lacksVariables: bool
        self.lacksVariables = lacksVariables

    def evaluate(
        self: Expression,
        variableValues: VariableValues
    ) -> Real:
        self._resetEvaluationCache()
        return self._evaluate(variableValues)

    def deriveSingle(
        self: Expression,
        variableValues: VariableValues,
        withRespectTo: Variable,
    ) -> SingleResult:
        return self._deriveSingle(variableValues, withRespectTo).toSingleResult()

    def deriveMulti(
        self: Expression,
        variableValues: VariableValues
    ) -> MultiResult:
        self._resetEvaluationCache()
        value = self._evaluate(variableValues)
        multiResult = InternalMultiResult(value)
        self._deriveMulti(multiResult, variableValues, 1)
        return multiResult.toMultiResult()

    ## Abstract methods ##

    @abstractmethod
    def _resetEvaluationCache(
        self: Expression
    ) -> None:
        raise Exception("Concrete classes derived from Expression must implement _resetEvaluationCache()")

    @abstractmethod
    def _evaluate(
        self: Expression,
        variableValues: VariableValues
    ) -> Real:
        raise Exception("Concrete classes derived from Expression must implement _evaluate()")

    @abstractmethod
    def _deriveSingle(
        self: Expression,
        variableValues: VariableValues,
        withRespectTo: Variable
    ) -> InternalSingleResult:
        raise Exception("Concrete classes derived from Expression must implement _deriveSingle()")

    @abstractmethod
    def _deriveMulti(
        self: Expression,
        multiResult: InternalMultiResult,
        variableValues: VariableValues,
        seed: Real
    ) -> None:
        raise Exception("Concrete classes derived from Expression must implement _deriveMulti()")

    ## Operations ##

    def __neg__(
        self: Expression
    ) -> Negation:
        return Negation(self)

    def __add__(
        self: Expression,
        other: Expression
    ) -> Plus:
        return Plus(self, other)

    def __sub__(
        self: Expression,
        other: Expression
    ) -> Minus:
        return Minus(self, other)

    def __mul__(
        self: Expression,
        other: Expression
    ) -> Multiply:
        return Multiply(self, other)

    def __truediv__(
        self: Expression,
        other: Expression
    ) -> Divide:
        return Divide(self, other)

    def __pow__(
        self: Expression,
        other: Expression
    ) -> Power:
        return Power(self, other)

from src.smooth_expression.negation import Negation
from src.smooth_expression.plus import Plus
from src.smooth_expression.minus import Minus
from src.smooth_expression.multiply import Multiply
from src.smooth_expression.divide import Divide
from src.smooth_expression.power import Power
