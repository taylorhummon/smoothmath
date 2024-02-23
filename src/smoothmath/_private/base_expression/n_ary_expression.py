from __future__ import annotations
from typing import TYPE_CHECKING, Any, Callable, Optional
from abc import abstractmethod
import smoothmath._private.base_expression as base
import smoothmath._private.utilities as util
if TYPE_CHECKING:
    from smoothmath import Point, Expression


class NAryExpression(base.Expression):
    def __init__(
        self: NAryExpression,
        *args: Expression
    ) -> None:
        for inner in args:
            if not isinstance(inner, base.Expression):
                raise Exception(f"Expressions must be composed of Expressions, found: {inner}")
        variable_names = set().union(*(inner._variable_names for inner in args))
        super().__init__(variable_names)
        self._inners: list[Expression]
        self._inners = list(args)
        self._value: Optional[float]
        self._value = None

    def _rebuild(
        self: NAryExpression,
        *args: Expression
    ) -> NAryExpression:
        return self.__class__(*args)

    ## Evaluation ##

    def _reset_evaluation_cache(
        self: NAryExpression
    ) -> None:
        self._value = None
        for inner in self._inners:
            inner._reset_evaluation_cache()

    def _evaluate(
        self: NAryExpression,
        point: Point
    ) -> float:
        if self._value is not None:
            return self._value
        inner_values = [inner._evaluate(point) for inner in self._inners]
        self._verify_domain_constraints(*inner_values)
        self._value = self._value_formula(*inner_values)
        return self._value

    @abstractmethod
    def _verify_domain_constraints(
        self: NAryExpression,
        *inner_values: float
    ) -> None:
        raise Exception("Concrete classes derived from NAryExpression must implement _verify_domain_constraints()")

    @abstractmethod
    def _value_formula(
        self: NAryExpression,
        *inner_values: float
    ) -> float:
        raise Exception("Concrete classes derived from NAryExpression must implement _value_formula()")

    ## Normalization and Reduction ##

    def _take_reduction_step(
        self: NAryExpression
    ) -> Expression:
        if self._is_fully_reduced:
            return self
        consolidated = self._consolidate_expression_lacking_variables()
        if consolidated is not None:
            return consolidated
        for (i, inner) in enumerate(self._inners):
            if not inner._is_fully_reduced:
                reduced_inner = inner._take_reduction_step()
                revised = util.list_with_updated_entry_at(self._inners, i, reduced_inner)
                return self._rebuild(*revised)
        for reducer in self._reducers:
            reduced = reducer()
            if reduced is not None:
                return reduced
        self._is_fully_reduced = True
        return self

    @property
    @abstractmethod
    def _reducers(
        self: NAryExpression
    ) -> list[Callable[[], Optional[Expression]]]:
        raise Exception("Concrete classes derived from NAryExpression must implement _reducers()")

    def _normalize_fully_reduced(
        self: NAryExpression
    ) -> Expression:
        normalized_inners = (inner._normalize_fully_reduced() for inner in self._inners)
        return self._rebuild(*normalized_inners)

    ## Operations ##

    def __eq__(
        self: NAryExpression,
        other: Any
    ) -> bool:
        if other.__class__ != self.__class__:
            return False
        if len(other._inners) != len(self._inners):
            return False
        if any(a != b for (a, b) in zip(other._inners, self._inners)):
            return False
        return True

    def __hash__(
        self: NAryExpression
    ) -> int:
        return hash((
            util.get_class_name(self),
            len(self._inners),
            tuple(self._inners)
        ))

    def __str__(
        self: NAryExpression
    ) -> str:
        inner_strings = ", ".join(str(inner) for inner in self._inners)
        return f"{util.get_class_name(self)}({inner_strings})"

    def __repr__(
        self: NAryExpression
    ) -> str:
        inner_strings = ", ".join(str(inner) for inner in self._inners)
        return f"{util.get_class_name(self)}({inner_strings})"
