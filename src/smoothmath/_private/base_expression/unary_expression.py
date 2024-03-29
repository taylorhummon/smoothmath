from __future__ import annotations
from typing import TYPE_CHECKING, Any, Callable, Optional
from abc import abstractmethod
import smoothmath._private.base_expression as base
import smoothmath._private.utilities as util
if TYPE_CHECKING:
    from smoothmath import Point, Expression
    from smoothmath._private.accumulators import (
        NumericPartialsAccumulator, SyntheticPartialsAccumulator
    )


class UnaryExpression(base.Expression):
    def __init__(
        self: UnaryExpression,
        inner: Expression
    ) -> None:
        if not isinstance(inner, base.Expression):
            raise Exception(f"Expressions must be composed of Expressions, found: {inner}")
        super().__init__(inner._variable_names)
        self._inner: Expression
        self._inner = inner
        self._value: Optional[float]
        self._value = None

    def _rebuild(
        self: UnaryExpression,
        inner: Expression
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
        point: Point
    ) -> float:
        if self._value is not None:
            return self._value
        inner_value = self._inner._evaluate(point)
        self._verify_domain_constraints(inner_value)
        self._value = self._value_formula(inner_value)
        return self._value

    @abstractmethod
    def _verify_domain_constraints(
        self: UnaryExpression,
        inner_value: float
    ) -> None:
        raise Exception("Concrete classes derived from UnaryExpression must implement _verify_domain_constraints()")

    @abstractmethod
    def _value_formula(
        self: UnaryExpression,
        inner_value: float
    ) -> float:
        raise Exception("Concrete classes derived from UnaryExpression must implement _value_formula()")

    ## Partials ##

    def _numeric_partial(
        self: UnaryExpression,
        variable_name: str,
        point: Point
    ) -> float:
        inner_value = self._inner._evaluate(point)
        self._verify_domain_constraints(inner_value)
        inner_partial = self._inner._numeric_partial(variable_name, point)
        return self._numeric_partial_formula(point, inner_partial)

    def _synthetic_partial(
        self: UnaryExpression,
        variable_name: str
    ) -> Expression:
        inner_partial = self._inner._synthetic_partial(variable_name)
        return self._synthetic_partial_formula(inner_partial)

    def _compute_numeric_partials(
        self: UnaryExpression,
        accumulator: NumericPartialsAccumulator,
        multiplier: float,
        point: Point
    ) -> None:
        inner_value = self._inner._evaluate(point)
        self._verify_domain_constraints(inner_value)
        next_multiplier = self._numeric_partial_formula(point, multiplier)
        self._inner._compute_numeric_partials(accumulator, next_multiplier, point)

    def _compute_synthetic_partials(
        self: UnaryExpression,
        accumulator: SyntheticPartialsAccumulator,
        multiplier: Expression
    ) -> None:
        next_multiplier = self._synthetic_partial_formula(multiplier)
        self._inner._compute_synthetic_partials(accumulator, next_multiplier)

    @abstractmethod
    def _numeric_partial_formula(
        self: UnaryExpression,
        point: Point,
        multiplier: float
    ) -> float:
        raise Exception("Concrete classes derived from UnaryExpression must implement _numeric_partial_formula()")

    @abstractmethod
    def _synthetic_partial_formula(
        self: UnaryExpression,
        multiplier: Expression
    ) -> Expression:
        raise Exception("Concrete classes derived from UnaryExpression must implement _synthetic_partial_formula()")

    ## Normalization and Reduction ##

    def _take_reduction_step(
        self: UnaryExpression
    ) -> Expression:
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
    ) -> list[Callable[[], Optional[Expression]]]:
        raise Exception("Concrete classes derived from UnaryExpression must implement _reducers()")

    def _normalize_fully_reduced(
        self: UnaryExpression
    ) -> Expression:
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
        return hash((util.get_class_name(self), self._inner))

    def __str__(
        self: UnaryExpression
    ) -> str:
        return f"{util.get_class_name(self)}({self._inner})"

    def __repr__(
        self: UnaryExpression
    ) -> str:
        return f"{util.get_class_name(self)}({self._inner})"
