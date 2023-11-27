from __future__ import annotations
from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:
    from smoothmath.types import real_number
    from smoothmath.expressions import Variable

from abc import ABC, abstractmethod
import smoothmath.utilities as utilities
from smoothmath.point import Point
from smoothmath.computed_local_partials import ComputedLocalPartials
from smoothmath.computed_global_partials import ComputedGlobalPartials
import smoothmath.expressions as ex


class Expression(ABC):
    def __init__(
        self: Expression,
        lacks_variables: bool
    ) -> None:
        self._lacks_variables: bool
        self._lacks_variables = lacks_variables

    def evaluate(
        self: Expression,
        point: Point
    ) -> real_number:
        if not isinstance(point, Point):
            raise Exception("Must provide a Point to evaluate()")
        self._reset_evaluation_cache()
        return self._evaluate(point)

    def partial_at(
        self: Expression,
        point: Point,
        with_respect_to: Variable | str
    ) -> real_number:
        if not isinstance(point, Point):
            raise Exception("Must provide a Point to partial_at()")
        self._reset_evaluation_cache()
        variable_name = utilities.get_variable_name(with_respect_to)
        return self._partial_at(point, variable_name)

    def compute_local_partials(
        self: Expression,
        point: Point
    ) -> ComputedLocalPartials:
        if not isinstance(point, Point):
            raise Exception("Must provide a Point to compute_local_partials()")
        self._reset_evaluation_cache()
        computed_local_partials = ComputedLocalPartials()
        self._compute_local_partials(computed_local_partials, point, 1)
        return computed_local_partials

    def compute_global_partials(
        self: Expression
    ) -> ComputedGlobalPartials:
        computed_global_partials = ComputedGlobalPartials(original_expression = self)
        self._compute_global_partials(computed_global_partials, ex.Constant(1))
        return computed_global_partials


    ## Abstract methods ##

    @abstractmethod
    def _reset_evaluation_cache(
        self: Expression
    ) -> None:
        raise Exception("Concrete classes derived from Expression must implement _reset_evaluation_cache()")

    @abstractmethod
    def _evaluate(
        self: Expression,
        point: Point
    ) -> real_number:
        raise Exception("Concrete classes derived from Expression must implement _evaluate()")

    @abstractmethod
    def _partial_at(
        self: Expression,
        point: Point,
        with_respect_to: str
    ) -> real_number:
        raise Exception("Concrete classes derived from Expression must implement _partial_at()")

    @abstractmethod
    def _compute_local_partials(
        self: Expression,
        computed_local_partials: ComputedLocalPartials,
        point: Point,
        accumulated: real_number
    ) -> None: # instead of returning a value, we mutate the computed_local_partials argument
        raise Exception("Concrete classes derived from Expression must implement _compute_local_partials()")

    @abstractmethod
    def _global_partial(
        self: Expression,
        with_respect_to: str
    ) -> Expression:
        raise Exception("Concrete classes derived from Expression must implement _global_partial()")

    @abstractmethod
    def _compute_global_partials(
        self: Expression,
        computed_global_partials: ComputedGlobalPartials,
        accumulated: Expression
    ) -> None: # instead of returning a value, we mutate the computed_global_partials argument
        raise Exception("Concrete classes derived from Expression must implement _compute_global_partials()")


    ## Operations ##

    def __neg__(
        self: Expression
    ) -> ex.Negation:
        return ex.Negation(self)

    def __add__(
        self: Expression,
        other: Expression
    ) -> ex.Plus:
        return ex.Plus(self, other)

    def __sub__(
        self: Expression,
        other: Expression
    ) -> ex.Minus:
        return ex.Minus(self, other)

    def __mul__(
        self: Expression,
        other: Expression
    ) -> ex.Multiply:
        return ex.Multiply(self, other)

    def __truediv__(
        self: Expression,
        other: Expression
    ) -> ex.Divide:
        return ex.Divide(self, other)

    def __pow__(
        self: Expression,
        other: Expression
    ) -> ex.Power:
        return ex.Power(self, other)


class NullaryExpression(Expression):
    def __init__(
        self: NullaryExpression,
        lacks_variables: bool
    ) -> None:
        super().__init__(lacks_variables)

    def _reset_evaluation_cache(
        self: NullaryExpression
    ) -> None:
        pass


class UnaryExpression(Expression):
    def __init__(
        self: UnaryExpression,
        a: Expression
    ) -> None:
        if not isinstance(a, Expression):
            raise Exception(f"Expressions must be composed of Expressions, found {a}")
        super().__init__(lacks_variables = a._lacks_variables)
        self._a: Expression
        self._a = a
        self._value: real_number | None
        self._value = None

    def _reset_evaluation_cache(
        self: UnaryExpression
    ) -> None:
        self._value = None
        self._a._reset_evaluation_cache()

    def __eq__(
        self: UnaryExpression,
        other: Any
    ) -> bool:
        return other.__class__ == self.__class__ and (other._a == self._a)

    def __str__(
        self: UnaryExpression
    ) -> str:
        class_name = type(self).__name__
        return f"{class_name}({self._a})"


class BinaryExpression(Expression):
    def __init__(
        self: BinaryExpression,
        a: Expression,
        b: Expression
    ) -> None:
        if not isinstance(a, Expression):
            raise Exception(f"Expressions must be composed of Expressions, found {a}")
        if not isinstance(b, Expression):
            raise Exception(f"Expressions must be composed of Expressions, found {b}")
        super().__init__(lacks_variables = a._lacks_variables and b._lacks_variables)
        self._a: Expression
        self._a = a
        self._b: Expression
        self._b = b
        self._value: real_number | None
        self._value = None

    def _reset_evaluation_cache(
        self: BinaryExpression
    ) -> None:
        self._value = None
        self._a._reset_evaluation_cache()
        self._b._reset_evaluation_cache()

    def __eq__(
        self: BinaryExpression,
        other: Any
    ) -> bool:
        return (
            (other.__class__ == self.__class__) and
            (other._a == self._a) and
            (other._b == self._b)
        )

    def __str__(
        self: BinaryExpression
    ) -> str:
        class_name = type(self).__name__
        return f"{class_name}({self._a}, {self._b})"
