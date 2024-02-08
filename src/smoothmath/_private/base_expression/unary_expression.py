from __future__ import annotations
from typing import TYPE_CHECKING, Any, Callable
from abc import abstractmethod
import smoothmath as sm
import smoothmath._private.base_expression as base
from smoothmath._private.utilities import get_class_name
if TYPE_CHECKING:
    from smoothmath import RealNumber
    from smoothmath._private.local_differential import LocalDifferentialBuilder
    from smoothmath._private.global_differential import GlobalDifferentialBuilder


class UnaryExpression(base.Expression):
    def __init__(
        self: UnaryExpression,
        inner: sm.Expression
    ) -> None:
        if not isinstance(inner, sm.Expression):
            raise Exception(f"Expressions must be composed of Expressions, found: {inner}")
        super().__init__(inner._lacks_variables)
        self._inner: sm.Expression
        self._inner = inner
        self._value: RealNumber | None
        self._value = None

    def _rebuild(
        self: UnaryExpression,
        inner: sm.Expression
    ) -> UnaryExpression:
        return self.__class__(inner)

    ## Evaluation ##

    def _reset_evaluation_cache(
        self: UnaryExpression
    ) -> None:
        self._value = None
        self._inner._reset_evaluation_cache()

    def _evaluate(
        self: UnaryExpression,
        point: sm.Point
    ) -> RealNumber:
        if self._value is not None:
            return self._value
        inner_value = self._inner._evaluate(point)
        self._verify_domain_constraints(inner_value)
        self._value = self._value_formula(inner_value)
        return self._value

    @abstractmethod
    def _verify_domain_constraints(
        self: UnaryExpression,
        inner_value: RealNumber
    ) -> None:
        raise Exception("Concrete classes derived from UnaryExpression must implement _verify_domain_constraints()")

    @abstractmethod
    def _value_formula(
        self: UnaryExpression,
        inner_value: RealNumber
    ) -> RealNumber:
        raise Exception("Concrete classes derived from UnaryExpression must implement _value_formula()")

    ## Partials and Differentials ##

    def _local_partial(
        self: UnaryExpression,
        point: sm.Point,
        with_respect_to: str
    ) -> RealNumber:
        inner_value = self._inner._evaluate(point)
        self._verify_domain_constraints(inner_value)
        inner_partial = self._inner._local_partial(point, with_respect_to)
        return self._local_partial_formula(point, inner_partial)

    def _synthetic_partial(
        self: UnaryExpression,
        with_respect_to: str
    ) -> sm.Expression:
        inner_partial = self._inner._synthetic_partial(with_respect_to)
        return self._synthetic_partial_formula(inner_partial)

    def _compute_local_differential(
        self: UnaryExpression,
        builder: LocalDifferentialBuilder,
        accumulated: RealNumber
    ) -> None:
        inner_value = self._inner._evaluate(builder.point)
        self._verify_domain_constraints(inner_value)
        next_accumulated = self._local_partial_formula(builder.point, accumulated)
        self._inner._compute_local_differential(builder, next_accumulated)

    def _compute_global_differential(
        self: UnaryExpression,
        builder: GlobalDifferentialBuilder,
        accumulated: sm.Expression
    ) -> None:
        next_accumulated = self._synthetic_partial_formula(accumulated)
        self._inner._compute_global_differential(builder, next_accumulated)

    @abstractmethod
    def _local_partial_formula(
        self: UnaryExpression,
        point: sm.Point,
        multiplier: RealNumber
    ) -> RealNumber:
        raise Exception("Concrete classes derived from UnaryExpression must implement _local_partial_formula()")

    @abstractmethod
    def _synthetic_partial_formula(
        self: UnaryExpression,
        multiplier: sm.Expression
    ) -> sm.Expression:
        raise Exception("Concrete classes derived from UnaryExpression must implement _synthetic_partial_formula()")

    ## Normalization and Reduction ##

    def _take_reduction_step(
        self: UnaryExpression
    ) -> sm.Expression:
        if self._is_fully_reduced:
            return self
        consolidated = self._consolidate_expression_lacking_variables()
        if consolidated is not None:
            return consolidated
        if not self._inner._is_fully_reduced:
            reduced_inner = self._inner._take_reduction_step()
            return self._rebuild(reduced_inner)
        for reducer in self._reducers:
            reduced = reducer()
            if reduced is not None:
                return reduced
        self._is_fully_reduced = True
        return self

    @property
    @abstractmethod
    def _reducers(
        self: UnaryExpression
    ) -> list[Callable[[], sm.Expression | None]]:
        raise Exception("Concrete classes derived from UnaryExpression must implement _reducers()")

    def _normalize_fully_reduced(
        self: UnaryExpression
    ) -> sm.Expression:
        normalized_inner = self._inner._normalize_fully_reduced()
        return self._rebuild(normalized_inner)

    ## Operations ##

    def __eq__(
        self: UnaryExpression,
        other: Any
    ) -> bool:
        return (other.__class__ == self.__class__) and (other._inner == self._inner)

    def __hash__(
        self: UnaryExpression
    ) -> int:
        return hash((get_class_name(self), self._inner))

    def __str__(
        self: UnaryExpression
    ) -> str:
        return f"{get_class_name(self)}({self._inner})"

    def __repr__(
        self: UnaryExpression
    ) -> str:
        return f"{get_class_name(self)}({self._inner})"
