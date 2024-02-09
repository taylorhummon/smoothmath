from __future__ import annotations
from typing import TYPE_CHECKING, Any, Callable, Optional
from abc import abstractmethod
import smoothmath as sm
import smoothmath._private.base_expression as base
from smoothmath._private.utilities import get_class_name, list_with_updated_entry_at
if TYPE_CHECKING:
    from smoothmath import RealNumber


class NAryExpression(base.Expression):
    def __init__(
        self: NAryExpression,
        *args: sm.Expression
    ) -> None:
        for inner in args:
            if not isinstance(inner, sm.Expression):
                raise Exception(f"Expressions must be composed of Expressions, found: {inner}")
        lacks_variables = all(inner._lacks_variables for inner in args)
        super().__init__(lacks_variables)
        self._inners: list[sm.Expression]
        self._inners = list(args)
        self._value: Optional[RealNumber]
        self._value = None

    def _rebuild(
        self: NAryExpression,
        *args: sm.Expression
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
        point: sm.Point
    ) -> RealNumber:
        if self._value is not None:
            return self._value
        inner_values = [inner._evaluate(point) for inner in self._inners]
        self._verify_domain_constraints(*inner_values)
        self._value = self._value_formula(*inner_values)
        return self._value

    @abstractmethod
    def _verify_domain_constraints(
        self: NAryExpression,
        *inner_values: RealNumber
    ) -> None:
        raise Exception("Concrete classes derived from NAryExpression must implement _verify_domain_constraints()")

    @abstractmethod
    def _value_formula(
        self: NAryExpression,
        *inner_values: RealNumber
    ) -> RealNumber:
        raise Exception("Concrete classes derived from NAryExpression must implement _value_formula()")

    ## Normalization and Reduction ##

    def _take_reduction_step(
        self: NAryExpression
    ) -> sm.Expression:
        if self._is_fully_reduced:
            return self
        consolidated = self._consolidate_expression_lacking_variables()
        if consolidated is not None:
            return consolidated
        for (i, inner) in enumerate(self._inners):
            if not inner._is_fully_reduced:
                reduced_inner = inner._take_reduction_step()
                revised = list_with_updated_entry_at(self._inners, i, reduced_inner)
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
    ) -> list[Callable[[], Optional[sm.Expression]]]:
        raise Exception("Concrete classes derived from NAryExpression must implement _reducers()")

    def _normalize_fully_reduced(
        self: NAryExpression
    ) -> sm.Expression:
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
            get_class_name(self),
            len(self._inners),
            tuple(self._inners)
        ))

    def __str__(
        self: NAryExpression
    ) -> str:
        inner_strings = ", ".join(str(inner) for inner in self._inners)
        return f"{get_class_name(self)}({inner_strings})"

    def __repr__(
        self: NAryExpression
    ) -> str:
        inner_strings = ", ".join(str(inner) for inner in self._inners)
        return f"{get_class_name(self)}({inner_strings})"
