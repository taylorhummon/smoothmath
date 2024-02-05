from __future__ import annotations
from typing import TYPE_CHECKING, Any
import smoothmath as sm
import smoothmath.expression as ex
import smoothmath._private.base_expression as base
if TYPE_CHECKING:
    from smoothmath._private.local_differential import LocalDifferentialBuilder
    from smoothmath._private.global_differential import GlobalDifferentialBuilder


class Constant(base.Expression):
    def __init__(
        self: Constant,
        value: sm.real_number
    ) -> None:
        super().__init__(lacks_variables = True)
        self.value: sm.real_number
        self.value = value

    ## Evaluation ##

    def _reset_evaluation_cache(
        self: Constant
    ) -> None:
        pass

    def _evaluate(
        self: Constant,
        point: sm.Point
    ) -> sm.real_number:
        return self.value

    ## Partials and Differentials ##

    def _local_partial(
        self: Constant,
        point: sm.Point,
        with_respect_to: str
    ) -> sm.real_number:
        return 0

    def _synthetic_partial(
        self: Constant,
        with_respect_to: str
    ) -> sm.Expression:
        return ex.Constant(0)

    def _compute_local_differential(
        self: Constant,
        builder: LocalDifferentialBuilder,
        accumulated: sm.real_number
    ) -> None:
        pass

    def _compute_global_differential(
        self: Constant,
        builder: GlobalDifferentialBuilder,
        accumulated: sm.Expression
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
    ) -> sm.Expression:
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
