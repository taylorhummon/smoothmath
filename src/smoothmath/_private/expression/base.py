from __future__ import annotations
from typing import Any
from abc import ABC, abstractmethod
import smoothmath as sm
import smoothmath.expression as ex
from smoothmath._private.local_differential import LocalDifferentialBuilder
from smoothmath._private.global_differential import GlobalDifferentialBuilder
from smoothmath._private.utilities import (
  integer_from_integral_real_number,
  get_class_name,
  get_variable_name
)


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
        self._compute_local_differential(builder, 1)
        return builder.build()

    def global_differential(
        self: Expression
    ) -> sm.GlobalDifferential:
        builder = GlobalDifferentialBuilder(self)
        self._compute_global_differential(builder, ex.Constant(1))
        return builder.build()

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
        exponent: int | Expression
    ) -> ex.NthPower | ex.Power:
        if isinstance(exponent, Expression):
            return ex.Power(self, exponent)
        # We want to allow a user to pass a float representation of an integer (e.g. 3.0)
        # even though that wouldn't pass type checking.
        integer = integer_from_integral_real_number(exponent)
        if integer is None:
            raise Exception(f"Expected exponent to be an Expression or int, found: {exponent}")
        else:
            return ex.NthPower(integer, self)

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
        inner: Expression
    ) -> None:
        if not isinstance(inner, Expression):
            raise Exception(f"Expressions must be composed of Expressions, found {inner}")
        super().__init__(inner._lacks_variables)
        self._inner: Expression
        self._inner = inner
        self._value: sm.real_number | None
        self._value = None

    def _rebuild(
        self: UnaryExpression,
        inner: sm.Expression
    ) -> UnaryExpression:
        return self.__class__(inner)

    def _reset_evaluation_cache(
        self: UnaryExpression
    ) -> None:
        self._value = None
        self._inner._reset_evaluation_cache()

    def _evaluate(
        self: UnaryExpression,
        point: sm.Point
    ) -> sm.real_number:
        if self._value is not None:
            return self._value
        inner_value = self._inner._evaluate(point)
        self._verify_domain_constraints(inner_value)
        self._value = self._value_formula(inner_value)
        return self._value

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

    ## Abstract methods ##

    @abstractmethod
    def _verify_domain_constraints(
        self: UnaryExpression,
        inner_value: sm.real_number
    ) -> None:
        raise Exception("Concrete classes derived from UnaryExpression must implement _verify_domain_constraints()")

    @abstractmethod
    def _value_formula(
        self: UnaryExpression,
        inner_value: sm.real_number
    ) -> sm.real_number:
        raise Exception("Concrete classes derived from UnaryExpression must implement _value_formula()")


class ParameterizedUnaryExpression(Expression):
    def __init__(
        self: ParameterizedUnaryExpression,
        inner: Expression
    ) -> None:
        if not isinstance(inner, Expression):
            raise Exception(f"Expressions must be composed of Expressions, found {inner}")
        super().__init__(inner._lacks_variables)
        self._inner: Expression
        self._inner = inner
        self._value: sm.real_number | None
        self._value = None

    def _rebuild(
        self: ParameterizedUnaryExpression,
        inner: sm.Expression
    ) -> ParameterizedUnaryExpression:
        return self.__class__(self._parameter(), inner) # type: ignore

    def _reset_evaluation_cache(
        self: ParameterizedUnaryExpression
    ) -> None:
        self._value = None
        self._inner._reset_evaluation_cache()

    def _evaluate(
        self: ParameterizedUnaryExpression,
        point: sm.Point
    ) -> sm.real_number:
        if self._value is not None:
            return self._value
        inner_value = self._inner._evaluate(point)
        self._verify_domain_constraints(inner_value)
        self._value = self._value_formula(inner_value)
        return self._value

    ## Operations ##

    def __eq__(
        self: ParameterizedUnaryExpression,
        other: Any
    ) -> bool:
        return (
            (other.__class__ == self.__class__) and
            (other._parameter() == self._parameter()) and
            (other._inner == self._inner)
        )

    def __hash__(
        self: ParameterizedUnaryExpression
    ) -> int:
        return hash((get_class_name(self), self._parameter(), self._inner))

    def __str__(
        self: ParameterizedUnaryExpression
    ) -> str:
        return f"{get_class_name(self)}({self._parameter()}, {self._inner})"

    def __repr__(
        self: ParameterizedUnaryExpression
    ) -> str:
        return f"{get_class_name(self)}({self._parameter()}, {self._inner})"

    ## Abstract methods ##

    @abstractmethod
    def _parameter(
        self: ParameterizedUnaryExpression
    ) -> Any:
        raise Exception("Concrete classes derived from ParameterizedUnaryExpression must implement _parameter()")

    @abstractmethod
    def _verify_domain_constraints(
        self: ParameterizedUnaryExpression,
        inner_value: sm.real_number
    ) -> None:
        raise Exception("Concrete classes derived from ParameterizedUnaryExpression must implement _verify_domain_constraints()")

    @abstractmethod
    def _value_formula(
        self: ParameterizedUnaryExpression,
        inner_value: sm.real_number
    ) -> sm.real_number:
        raise Exception("Concrete classes derived from ParameterizedUnaryExpression must implement _value_formula()")


class BinaryExpression(Expression):
    def __init__(
        self: BinaryExpression,
        left: Expression,
        right: Expression
    ) -> None:
        if not isinstance(left, Expression):
            raise Exception(f"Expressions must be composed of Expressions, found {left}")
        if not isinstance(right, Expression):
            raise Exception(f"Expressions must be composed of Expressions, found {right}")
        super().__init__(left._lacks_variables and right._lacks_variables)
        self._left: Expression
        self._left = left
        self._right: Expression
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
