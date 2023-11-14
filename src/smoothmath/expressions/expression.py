from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from smoothmath.typing import real_number
    from smoothmath.expressions.variable import Variable

# imports needed for class declaration
from abc import ABC, abstractmethod


class Expression(ABC):
    def __init__(
        self: Expression,
        lacks_variables: bool
    ) -> None:
        self._lacks_variables: bool
        self._lacks_variables = lacks_variables

    def evaluate(
        self: Expression,
        variable_values: VariableValues
    ) -> real_number:
        if not isinstance(variable_values, VariableValues):
            raise Exception("Must provide a VariableValues object to evaluate()")
        self._reset_evaluation_cache()
        return self._evaluate(variable_values)

    def partial_at(
        self: Expression,
        variable_values: VariableValues,
        with_respect_to: Variable | str,
    ) -> real_number:
        if not isinstance(variable_values, VariableValues):
            raise Exception("Must provide a VariableValues object to partial_at()")
        self._reset_evaluation_cache()
        variableName = utilities.get_variable_name(with_respect_to)
        return self._partial_at(variable_values, variableName)

    def all_partials_at(
        self: Expression,
        variable_values: VariableValues
    ) -> AllPartials:
        if not isinstance(variable_values, VariableValues):
            raise Exception("Must provide a VariableValues object to all_partials_at()")
        self._reset_evaluation_cache()
        all_partials = AllPartials()
        self._compute_all_partials_at(all_partials, variable_values, 1)
        return all_partials

    ## Abstract methods ##

    @abstractmethod
    def _reset_evaluation_cache(
        self: Expression
    ) -> None:
        raise Exception("Concrete classes derived from Expression must implement _reset_evaluation_cache()")

    @abstractmethod
    def _evaluate(
        self: Expression,
        variable_values: VariableValues
    ) -> real_number:
        raise Exception("Concrete classes derived from Expression must implement _evaluate()")

    @abstractmethod
    def _partial_at(
        self: Expression,
        variable_values: VariableValues,
        with_respect_to: str
    ) -> real_number:
        raise Exception("Concrete classes derived from Expression must implement _partial_at()")

    @abstractmethod
    def _compute_all_partials_at(
        self: Expression,
        all_partials: AllPartials,
        variable_values: VariableValues,
        seed: real_number
    ) -> None:
        raise Exception("Concrete classes derived from Expression must implement _compute_all_partials_at()")

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


# imports needed for class implementation
import smoothmath.utilities as utilities
from smoothmath.variable_values import VariableValues
from smoothmath.all_partials import AllPartials
from smoothmath.expressions.negation import Negation
from smoothmath.expressions.plus import Plus
from smoothmath.expressions.minus import Minus
from smoothmath.expressions.multiply import Multiply
from smoothmath.expressions.divide import Divide
from smoothmath.expressions.power import Power
