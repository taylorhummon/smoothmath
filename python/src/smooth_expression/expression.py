from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.smooth_expression.custom_types import Real, VariableOrString
from abc import ABC, abstractmethod
from src.smooth_expression.utilities import _nameFromVariableOrName
from src.smooth_expression.variable_values import VariableValues
from src.smooth_expression.all_partials import AllPartials

class Expression(ABC):
    def __init__(
        self: Expression,
        lacksVariables: bool
    ) -> None:
        self.lacksVariables : bool
        self.lacksVariables = lacksVariables

    def evaluate(
        self: Expression,
        variableValues: VariableValues
    ) -> Real:
        if not isinstance(variableValues, VariableValues):
            raise Exception("Must provide a VariableValues object to evaluate()")
        self._resetEvaluationCache()
        return self._evaluate(variableValues)

    def partialAt(
        self: Expression,
        variableValues: VariableValues,
        withRespectTo: VariableOrString,
    ) -> Real:
        if not isinstance(variableValues, VariableValues):
            raise Exception("Must provide a VariableValues object to partialAt()")
        self._resetEvaluationCache()
        _, partial = self._partialAt(variableValues, _nameFromVariableOrName(withRespectTo))
        return partial

    def allPartialsAt(
        self: Expression,
        variableValues: VariableValues
    ) -> AllPartials:
        if not isinstance(variableValues, VariableValues):
            raise Exception("Must provide a VariableValues object to allPartialsAt()")
        self._resetEvaluationCache()
        allPartials = AllPartials()
        self._allPartialsAt(allPartials, variableValues, 1)
        return allPartials

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
    def _partialAt(
        self: Expression,
        variableValues: VariableValues,
        withRespectTo: str
    ) -> tuple[bool, Real]:
        raise Exception("Concrete classes derived from Expression must implement _partialAt()")

    @abstractmethod
    def _allPartialsAt(
        self: Expression,
        allPartials: AllPartials,
        variableValues: VariableValues,
        seed: Real
    ) -> None:
        raise Exception("Concrete classes derived from Expression must implement _allPartialsAt()")

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
