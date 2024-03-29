from __future__ import annotations
from typing import TYPE_CHECKING, Any, Callable, Optional
from abc import abstractmethod
import smoothmath._private.base_expression as base
import smoothmath._private.utilities as util
if TYPE_CHECKING:
    from smoothmath import Point, Expression


class BinaryExpression(base.Expression):
    def __init__(
        self: BinaryExpression,
        left: Expression,
        right: Expression
    ) -> None:
        if not isinstance(left, base.Expression):
            raise Exception(f"Expressions must be composed of Expressions, found: {left}")
        if not isinstance(right, base.Expression):
            raise Exception(f"Expressions must be composed of Expressions, found: {right}")
        variable_names = left._variable_names.union(right._variable_names)
        super().__init__(variable_names)
        self._left: Expression
        self._left = left
        self._right: Expression
        self._right = right
        self._value: Optional[float]
        self._value = None

    def _rebuild(
        self: BinaryExpression,
        left: Expression,
        right: Expression
    ) -> BinaryExpression:
        return self.__class__(left, right)

    ## Evaluation ##

    def _reset_evaluation_cache(
        self: BinaryExpression
    ) -> None:
        self._value = None
        self._left._reset_evaluation_cache()
        self._right._reset_evaluation_cache()

    def _evaluate(
        self: BinaryExpression,
        point: Point
    ) -> float:
        if self._value is not None:
            return self._value
        left_value = self._left._evaluate(point)
        right_value = self._right._evaluate(point)
        self._verify_domain_constraints(left_value, right_value)
        self._value = self._value_formula(left_value, right_value)
        return self._value

    @abstractmethod
    def _verify_domain_constraints(
        self: BinaryExpression,
        left_value: float,
        right_value: float
    ) -> None:
        raise Exception("Concrete classes derived from BinaryExpression must implement _verify_domain_constraints()")

    @abstractmethod
    def _value_formula(
        self: BinaryExpression,
        left_value: float,
        right_value: float
    ) -> float:
        raise Exception("Concrete classes derived from BinaryExpression must implement _value_formula()")

    ## Normalization and Reduction ##

    def _take_reduction_step(
        self: BinaryExpression
    ) -> Expression:
        if self._is_fully_reduced:
            return self
        consolidated = self._consolidate_expression_lacking_variables()
        if consolidated is not None:
            return consolidated
        if not self._left._is_fully_reduced:
            reduced_left = self._left._take_reduction_step()
            return self._rebuild(reduced_left, self._right)
        if not self._right._is_fully_reduced:
            reduced_right = self._right._take_reduction_step()
            return self._rebuild(self._left, reduced_right)
        for reducer in self._reducers:
            reduced = reducer()
            if reduced is not None:
                return reduced
        self._is_fully_reduced = True
        return self

    @property
    @abstractmethod
    def _reducers(
        self: BinaryExpression
    ) -> list[Callable[[], Optional[Expression]]]:
        raise Exception("Concrete classes derived from BinaryExpression must implement _reducers()")

    def _normalize_fully_reduced(
        self: BinaryExpression
    ) -> Expression:
        normalized_left = self._left._normalize_fully_reduced()
        normalized_right = self._right._normalize_fully_reduced()
        return self._rebuild(normalized_left, normalized_right)

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
        return hash((util.get_class_name(self), self._left, self._right))

    def __str__(
        self: BinaryExpression
    ) -> str:
        return f"{util.get_class_name(self)}({self._left}, {self._right})"

    def __repr__(
        self: BinaryExpression
    ) -> str:
        return f"{util.get_class_name(self)}({self._left}, {self._right})"
