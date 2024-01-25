from __future__ import annotations
from typing import Any, Callable
from abc import abstractmethod
import smoothmath as sm
import smoothmath._private.base_expression as base
from smoothmath._private.utilities import get_class_name


class BinaryExpression(base.Expression):
    def __init__(
        self: BinaryExpression,
        left: sm.Expression,
        right: sm.Expression
    ) -> None:
        if not isinstance(left, sm.Expression):
            raise Exception(f"Expressions must be composed of Expressions, found: {left}")
        if not isinstance(right, sm.Expression):
            raise Exception(f"Expressions must be composed of Expressions, found: {right}")
        super().__init__(left._lacks_variables and right._lacks_variables)
        self._left: sm.Expression
        self._left = left
        self._right: sm.Expression
        self._right = right
        self._value: sm.real_number | None
        self._value = None

    def _rebuild(
        self: BinaryExpression,
        left: sm.Expression,
        right: sm.Expression
    ) -> BinaryExpression:
        return self.__class__(left, right)

    def _reset_evaluation_cache(
        self: BinaryExpression
    ) -> None:
        self._value = None
        self._left._reset_evaluation_cache()
        self._right._reset_evaluation_cache()

    def _evaluate(
        self: BinaryExpression,
        point: sm.Point
    ) -> sm.real_number:
        if self._value is not None:
            return self._value
        left_value = self._left._evaluate(point)
        right_value = self._right._evaluate(point)
        self._verify_domain_constraints(left_value, right_value)
        self._value = self._value_formula(left_value, right_value)
        return self._value

    def _take_reduction_step(
        self: BinaryExpression
    ) -> sm.Expression:
        if self._is_fully_reduced:
            return self
        if not self._left._is_fully_reduced:
            reduced_left = self._left._take_reduction_step()
            return self._rebuild(reduced_left, self._right)
        if not self._right._is_fully_reduced:
            reduced_right = self._right._take_reduction_step()
            return self._rebuild(self._left, reduced_right)
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
        self: BinaryExpression,
        other: Any
    ) -> bool:
        return (
            (other.__class__ == self.__class__) and
            (other._left == self._left) and
            (other._right == self._right)
        )

    def __hash__(
        self: BinaryExpression
    ) -> int:
        return hash((get_class_name(self), self._left, self._right))

    def __str__(
        self: BinaryExpression
    ) -> str:
        return f"{get_class_name(self)}({self._left}, {self._right})"

    def __repr__(
        self: BinaryExpression
    ) -> str:
        return f"{get_class_name(self)}({self._left}, {self._right})"

    ## Abstract methods ##

    @abstractmethod
    def _verify_domain_constraints(
        self: BinaryExpression,
        left_value: sm.real_number,
        right_value: sm.real_number
    ) -> None:
        raise Exception("Concrete classes derived from BinaryExpression must implement _verify_domain_constraints()")

    @abstractmethod
    def _value_formula(
        self: BinaryExpression,
        left_value: sm.real_number,
        right_value: sm.real_number
    ) -> sm.real_number:
        raise Exception("Concrete classes derived from BinaryExpression must implement _value_formula()")

    @property
    @abstractmethod
    def _reducers(
        self: BinaryExpression
    ) -> list[Callable[[], sm.Expression | None]]:
        raise Exception("Concrete classes derived from BinaryExpression must implement _reducers()")
