from __future__ import annotations
from typing import TYPE_CHECKING, Any
import re
import smoothmath._private.base_expression as base
import smoothmath._private.expression as ex
if TYPE_CHECKING:
    from smoothmath import Point, Expression
    from smoothmath._private.accumulators import (
        NumericPartialsAccumulator, SyntheticPartialsAccumulator
    )


ALPHANUMERIC_PATTERN = re.compile(r"\A\w*\Z")


class Variable(base.Expression):
    """
    A variable.

    >>> from smoothmath.expression import Variable
    >>> Variable("x")
    Variable("x")

    :param name: the variable's name
    """

    def __init__(
        self: Variable,
        name: str
    ) -> None:
        super().__init__(variable_names = {name})
        if (not name) or (ALPHANUMERIC_PATTERN.match(name) is None):
            raise Exception(f"Illegal variable name: {name}")
        self.name: str
        self.name = name

    def _rebuild(
        self: Variable
    ) -> Expression:
        return Variable(self.name)

    ## Evaluation ##

    def _reset_evaluation_cache(
        self: Variable
    ) -> None:
        pass

    def _evaluate(
        self: Variable,
        point: Point
    ) -> float:
        return point.coordinate(self.name)

    ## Partials ##

    def _numeric_partial(
        self: Variable,
        variable_name: str,
        point: Point
    ) -> float:
        if self.name == variable_name:
            return 1
        else:
            return 0

    def _synthetic_partial(
        self: Variable,
        variable_name: str
    ) -> Expression:
        if self.name == variable_name:
            return ex.Constant(1)
        else:
            return ex.Constant(0)

    def _compute_numeric_partials(
        self: Variable,
        accumulator: NumericPartialsAccumulator,
        multiplier: float,
        point: Point
    ) -> None:
        accumulator.add_to(self, multiplier)

    def _compute_synthetic_partials(
        self: Variable,
        accumulator: SyntheticPartialsAccumulator,
        multiplier: Expression
    ) -> None:
        accumulator.add_to(self, multiplier)

    ## Normalization and Reduction ##

    def _take_reduction_step(
        self: Variable
    ) -> Variable:
        self._is_fully_reduced = True
        return self

    def _normalize_fully_reduced(
        self: Variable
    ) -> Expression:
        return self._rebuild()

    ## Operations ##

    def __eq__(
        self: Variable,
        other: Any
    ) -> bool:
        return (other.__class__ == self.__class__) and (other.name == self.name)

    def __hash__(
        self: Variable
    ) -> int:
        return hash(("Variable", self.name))

    def __str__(
        self: Variable
    ) -> str:
        return f"Variable(\"{self.name}\")"

    def __repr__(
        self: Variable
    ) -> str:
        return f"Variable(\"{self.name}\")"


def get_variable_name(
    variable_or_name: Variable | str
) -> str:
    if isinstance(variable_or_name, str):
        return variable_or_name
    else:
        return variable_or_name.name
