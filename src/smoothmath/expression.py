from __future__ import annotations
from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:
    from smoothmath.types import real_number
    from smoothmath.expressions import Variable

from abc import ABC, abstractmethod
import smoothmath.utilities as utilities
from smoothmath.point import Point
from smoothmath.global_partial import GlobalPartial
from smoothmath.local_differential import LocalDifferential
from smoothmath.global_differential import GlobalDifferential
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

    def local_partial(
        self: Expression,
        point: Point,
        with_respect_to: Variable | str
    ) -> real_number:
        if not isinstance(point, Point):
            raise Exception("Must provide a Point to local_partial()")
        self._reset_evaluation_cache()
        variable_name = utilities.get_variable_name(with_respect_to)
        return self._local_partial(point, variable_name)

    def global_partial(
        self: Expression,
        with_respect_to: Variable | str
    ) -> GlobalPartial:
        variable_name = utilities.get_variable_name(with_respect_to)
        synthetic_partial = self._synthetic_partial(variable_name)
        return GlobalPartial(self, synthetic_partial)

    def local_differential(
        self: Expression,
        point: Point
    ) -> LocalDifferential:
        if not isinstance(point, Point):
            raise Exception("Must provide a Point to local_differential()")
        self._reset_evaluation_cache()
        local_differential = LocalDifferential(self)
        self._compute_local_differential(local_differential, point, 1)
        local_differential._freeze()
        return local_differential

    def global_differential(
        self: Expression
    ) -> GlobalDifferential:
        global_differential = GlobalDifferential(self)
        self._compute_global_differential(global_differential, ex.Constant(1))
        global_differential._freeze()
        return global_differential


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
    def _local_partial(
        self: Expression,
        point: Point,
        with_respect_to: str
    ) -> real_number:
        raise Exception("Concrete classes derived from Expression must implement _local_partial()")

    @abstractmethod
    def _synthetic_partial(
        self: Expression,
        with_respect_to: str
    ) -> Expression:
        raise Exception("Concrete classes derived from Expression must implement _synthetic_partial()")

    @abstractmethod
    def _compute_local_differential(
        self: Expression,
        local_differential: LocalDifferential,
        point: Point,
        accumulated: real_number
    ) -> None: # instead of returning a value, we mutate the local_differential argument
        raise Exception("Concrete classes derived from Expression must implement _compute_local_differential()")

    @abstractmethod
    def _compute_global_differential(
        self: Expression,
        global_differential: GlobalDifferential,
        accumulated: Expression
    ) -> None: # instead of returning a value, we mutate the global_differential argument
        raise Exception("Concrete classes derived from Expression must implement _compute_global_differential()")


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
