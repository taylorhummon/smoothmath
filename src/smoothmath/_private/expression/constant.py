from __future__ import annotations
from typing import TYPE_CHECKING, Any
import smoothmath._private.base_expression as base
import smoothmath._private.expression as ex
if TYPE_CHECKING:
    from smoothmath import Point, Expression
    from smoothmath._private.accumulators import (
        NumericPartialsAccumulator, SyntheticPartialsAccumulator
    )


class Constant(base.Expression):
    """
    A constant expression.

    >>> from smoothmath.expression import Constant
    >>> Constant(11)
    Constant(11)

    :param value: the real number value of the constant
    """
    def __init__(
        self: Constant,
        value: float
    ) -> None:
        super().__init__(variable_names = set())
        self.value: float
        self.value = value

    def _rebuild(
        self: Constant
    ) -> Expression:
        return Constant(self.value)

    ## Evaluation ##

    def _reset_evaluation_cache(
        self: Constant
    ) -> None:
        pass

    def _evaluate(
        self: Constant,
        point: Point
    ) -> float:
        return self.value

    ## Partials ##

    def _numeric_partial(
        self: Constant,
        variable_name: str,
        point: Point
    ) -> float:
        return 0

    def _synthetic_partial(
        self: Constant,
        variable_name: str
    ) -> Expression:
        return ex.Constant(0)

    def _compute_numeric_partials(
        self: Constant,
        accumulator: NumericPartialsAccumulator,
        multiplier: float,
        point: Point
    ) -> None:
        pass

    def _compute_synthetic_partials(
        self: Constant,
        accumulator: SyntheticPartialsAccumulator,
        multiplier: Expression
    ) -> None:
        pass

    ## Normalization and Reduction ##

    def _take_reduction_step(
        self: Constant
    ) -> Constant:
        self._is_fully_reduced = True
        return self

    def _normalize_fully_reduced(
        self: Constant
    ) -> Expression:
        return self._rebuild()

    ## Operations ##

    def __eq__(
        self: Constant,
        other: Any
    ) -> bool:
        return (other.__class__ == self.__class__) and (other.value == self.value)

    def __hash__(
        self: Constant
    ) -> int:
        return hash(("Constant", self.value))

    def __str__(
        self: Constant
    ) -> str:
        return f"Constant({self.value})"

    def __repr__(
        self: Constant
    ) -> str:
        return f"Constant({self.value})"
