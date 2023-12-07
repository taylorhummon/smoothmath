from __future__ import annotations
from typing import Any
from abc import ABC, abstractmethod
import smoothmath as sm
import smoothmath.expression as ex
from smoothmath._private.local_differential import LocalDifferentialBuilder
from smoothmath._private.global_differential import GlobalDifferentialBuilder
from smoothmath._private.utilities import get_class_name, get_variable_name


class Expression(ABC):
    def __init__(
        self: Expression,
        lacks_variables: bool
    ) -> None:
        self._lacks_variables: bool
        self._lacks_variables = lacks_variables

    def evaluate(
        self: Expression,
        point: sm.Point
    ) -> sm.real_number:
        if not isinstance(point, sm.Point):
            raise Exception("Must provide a Point to evaluate()")
        self._reset_evaluation_cache()
        return self._evaluate(point)

    def local_partial(
        self: Expression,
        point: sm.Point,
        with_respect_to: ex.Variable | str
    ) -> sm.real_number:
        if not isinstance(point, sm.Point):
            raise Exception("Must provide a Point to local_partial()")
        self._reset_evaluation_cache()
        variable_name = get_variable_name(with_respect_to)
        return self._local_partial(point, variable_name)

    def global_partial(
        self: Expression,
        with_respect_to: ex.Variable | str
    ) -> sm.GlobalPartial:
        variable_name = get_variable_name(with_respect_to)
        synthetic_partial = self._synthetic_partial(variable_name)
        return sm.GlobalPartial.build(self, synthetic_partial)

    def local_differential(
        self: Expression,
        point: sm.Point
    ) -> sm.LocalDifferential:
        if not isinstance(point, sm.Point):
            raise Exception("Must provide a Point to local_differential()")
        self._reset_evaluation_cache()
        builder = LocalDifferentialBuilder(self, point)
        self._compute_local_differential(builder, point, 1)
        return builder.build()

    def global_differential(
        self: Expression
    ) -> sm.GlobalDifferential:
        builder = GlobalDifferentialBuilder(self)
        self._compute_global_differential(builder, ex.Constant(1))
        return builder.build()


    ## Abstract methods ##

    @abstractmethod
    def _reset_evaluation_cache(
        self: Expression
    ) -> None:
        raise Exception("Concrete classes derived from Expression must implement _reset_evaluation_cache()")

    @abstractmethod
    def _evaluate(
        self: Expression,
        point: sm.Point
    ) -> sm.real_number:
        raise Exception("Concrete classes derived from Expression must implement _evaluate()")

    @abstractmethod
    def _local_partial(
        self: Expression,
        point: sm.Point,
        with_respect_to: str
    ) -> sm.real_number:
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
        builder: LocalDifferentialBuilder,
        point: sm.Point,
        accumulated: sm.real_number
    ) -> None: # instead of returning a value, we mutate the local_differential argument
        raise Exception("Concrete classes derived from Expression must implement _compute_local_differential()")

    @abstractmethod
    def _compute_global_differential(
        self: Expression,
        builder: GlobalDifferentialBuilder,
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
        self._value: sm.real_number | None
        self._value = None

    def _reset_evaluation_cache(
        self: UnaryExpression
    ) -> None:
        self._value = None
        self._a._reset_evaluation_cache()

    def _rebuild(
        self: UnaryExpression,
        a: sm.Expression
    ) -> UnaryExpression:
        return type(self)(a)

    def __eq__(
        self: UnaryExpression,
        other: Any
    ) -> bool:
        return (
            (type(other) == type(self)) and
            (other._a == self._a)
        )

    def __hash__(
        self: UnaryExpression
    ) -> int:
        return hash((get_class_name(self), hash(self._a)))

    def __str__(
        self: UnaryExpression
    ) -> str:
        return f"{get_class_name(self)}({self._a})"

    def __repr__(
        self: UnaryExpression
    ) -> str:
        return f"{get_class_name(self)}({self._a})"


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
        self._value: sm.real_number | None
        self._value = None

    def _reset_evaluation_cache(
        self: BinaryExpression
    ) -> None:
        self._value = None
        self._a._reset_evaluation_cache()
        self._b._reset_evaluation_cache()

    def _rebuild(
        self: BinaryExpression,
        a: sm.Expression,
        b: sm.Expression
    ) -> BinaryExpression:
        return type(self)(a, b)

    def __eq__(
        self: BinaryExpression,
        other: Any
    ) -> bool:
        return (
            (type(other) == type(self)) and
            (other._a == self._a) and
            (other._b == self._b)
        )

    def __hash__(
        self: BinaryExpression
    ) -> int:
        return hash((get_class_name(self), hash(self._a), hash(self._b)))

    def __str__(
        self: BinaryExpression
    ) -> str:
        return f"{get_class_name(self)}({self._a}, {self._b})"

    def __repr__(
        self: BinaryExpression
    ) -> str:
        return f"{get_class_name(self)}({self._a}, {self._b})"
