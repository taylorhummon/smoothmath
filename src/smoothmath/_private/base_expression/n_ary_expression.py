from __future__ import annotations
from typing import Any, Callable
from abc import abstractmethod
import smoothmath as sm
import smoothmath._private.base_expression as base
from smoothmath._private.utilities import get_class_name, list_with_updated_entry_at


class NAryExpression(base.Expression):
    def __init__(
        self: NAryExpression,
        inner_expressions: list[sm.Expression]
    ) -> None:
        for inner in inner_expressions:
            if not isinstance(inner, sm.Expression):
                raise Exception(f"Expressions must be composed of Expressions, found: {inner}")
        lacks_variables = all(inner._lacks_variables for inner in inner_expressions)
        super().__init__(lacks_variables)
        self._inner_expressions: list[sm.Expression]
        self._inner_expressions = inner_expressions
        self._value: sm.real_number | None
        self._value = None

    def _rebuild(
        self: NAryExpression,
        inner_expressions: list[sm.Expression]
    ) -> NAryExpression:
        return self.__class__(inner_expressions)

    def _reset_evaluation_cache(
        self: NAryExpression
    ) -> None:
        self._value = None
        for inner in self._inner_expressions:
            inner._reset_evaluation_cache()

    def _evaluate(
        self: NAryExpression,
        point: sm.Point
    ) -> sm.real_number:
        if self._value is not None:
            return self._value
        inner_values = [inner._evaluate(point) for inner in self._inner_expressions]
        self._verify_domain_constraints(inner_values)
        self._value = self._value_formula(inner_values)
        return self._value

    def _take_reduction_step(
        self: NAryExpression
    ) -> sm.Expression:
        if self._is_fully_reduced:
            return self
        for (i, inner) in enumerate(self._inner_expressions):
            if not inner._is_fully_reduced:
                reduced_inner = inner._take_reduction_step()
                revised = list_with_updated_entry_at(self._inner_expressions, i, reduced_inner)
                return self._rebuild(revised)
        reduced = self._reduce_when_lacking_variables()
        if reduced is not None:
            return reduced
        for reducer in self._reducers:
            reduced = reducer()
            if reduced is not None:
                return reduced
        self._is_fully_reduced = True
        return self

    ## Operations ##

    def __eq__(
        self: NAryExpression,
        other: Any
    ) -> bool:
        return (
            (other.__class__ == self.__class__) and
            (len(other._inner_expressions) == len(self._inner_expressions)) and
            all(
                inner_a == inner_b
                for (inner_a, inner_b) in zip(other._inner_expressions, self._inner_expressions)
            )
        )

    def __hash__(
        self: NAryExpression
    ) -> int:
        return hash((
            get_class_name(self),
            len(self._inner_expressions),
            self._inner_expressions
        ))

    def __str__(
        self: NAryExpression
    ) -> str:
        inner_strings = ", ".join(str(inner) for inner in self._inner_expressions)
        return f"{get_class_name(self)}([{inner_strings}])"

    def __repr__(
        self: NAryExpression
    ) -> str:
        inner_strings = ", ".join(str(inner) for inner in self._inner_expressions)
        return f"{get_class_name(self)}([{inner_strings}])"

    ## Abstract methods ##

    @abstractmethod
    def _verify_domain_constraints(
        self: NAryExpression,
        inner_values: list[sm.real_number]
    ) -> None:
        raise Exception("Concrete classes derived from NAryExpression must implement _verify_domain_constraints()")

    @abstractmethod
    def _value_formula(
        self: NAryExpression,
        inner_values: list[sm.real_number]
    ) -> sm.real_number:
        raise Exception("Concrete classes derived from NAryExpression must implement _value_formula()")

    @property
    @abstractmethod
    def _reducers(
        self: NAryExpression
    ) -> list[Callable[[], sm.Expression | None]]:
        raise Exception("Concrete classes derived from NAryExpression must implement _reducers()")
