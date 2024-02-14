from __future__ import annotations
from typing import TYPE_CHECKING, Any
import smoothmath._private.base_expression as base
import smoothmath._private.expression as ex
if TYPE_CHECKING:
    from smoothmath import RealNumber, Point, Expression
    from smoothmath._private.local_partials_accumulator import LocalPartialsAccumulator
    from smoothmath._private.synthetic_partials_accumulator import SyntheticPartialsAccumulator


class Constant(base.Expression):
    """
    A constant expression.

    :param value: the real number value of the constant
    """
    def __init__(
        self: Constant,
        value: RealNumber
    ) -> None:
        super().__init__(lacks_variables = True)
        self.value: RealNumber
        self.value = value

    ## Evaluation ##

    def _reset_evaluation_cache(
        self: Constant
    ) -> None:
        pass

    def _evaluate(
        self: Constant,
        point: Point
    ) -> RealNumber:
        return self.value

    ## Partials and Differentials ##

    def _local_partial(
        self: Constant,
        variable_name: str,
        point: Point
    ) -> RealNumber:
        return 0

    def _synthetic_partial(
        self: Constant,
        variable_name: str
    ) -> Expression:
        return ex.Constant(0)

    def _compute_local_differential(
        self: Constant,
        accumulator: LocalPartialsAccumulator,
        multiplier: RealNumber
    ) -> None:
        pass

    def _compute_global_differential(
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
        return self

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
