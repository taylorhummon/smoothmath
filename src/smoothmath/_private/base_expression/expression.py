from __future__ import annotations
from typing import TYPE_CHECKING, Any, Optional
from abc import ABC, abstractmethod
import logging
import smoothmath._private.errors as er
import smoothmath._private.point as pt
import smoothmath._private.expression as ex
import smoothmath._private.accumulators as acc
import smoothmath._private.utilities as util
if TYPE_CHECKING:
    from smoothmath import Point
    from smoothmath.expression import (
        Add, Minus, Negation, Multiply, Divide, Power, NthPower
    )
    from smoothmath._private.accumulators import (
        NumericPartialsAccumulator, SyntheticPartialsAccumulator
    )


REDUCTION_STEPS_BOUND = 1000


class Expression(ABC):
    """
    An abstract base class for all expresssions.
    See the :mod:`smoothmath.expression` module for concrete expression classes.
    """

    def __init__(
        self: Expression,
        variable_names: set[str]
    ) -> None:
        self._variable_names: set[str]
        self._variable_names = variable_names
        self._is_fully_reduced: bool
        self._is_fully_reduced = False
        self._evaluation_failed: bool
        self._evaluation_failed = False

    @abstractmethod
    def _rebuild(
        self: Expression
    ) -> Expression:
        raise Exception("Concrete classes derived from Expression must implement _rebuild()")

    ## Evaluation ##

    def at(
        self: Expression,
        point: Point | float
    ) -> float:
        """
        Evaluates the expression at a point.

        Will raise an exception if the point parameter is a float and the expression has more
        than one variable.

        :param point: where to evaluate
        """
        if isinstance(point, pt.Point):
            self._reset_evaluation_cache()
            return self._evaluate(point)
        else: # point is a float
            exception_message = "Can only evaluate using a number for an expression with one variable. Consider passing a Point() instead."
            variable_name = get_the_single_variable_name(self, exception_message)
            point = pt.point_on_number_line(variable_name, point)
            self._reset_evaluation_cache()
            return self._evaluate(point)

    @abstractmethod
    def _reset_evaluation_cache(
        self: Expression
    ) -> None:
        raise Exception("Concrete classes derived from Expression must implement _reset_evaluation_cache()")

    @abstractmethod
    def _evaluate(
        self: Expression,
        point: Point
    ) -> float:
        raise Exception("Concrete classes derived from Expression must implement _evaluate()")

    ## Partials ##

    @abstractmethod
    def _numeric_partial(
        self: Expression,
        variable_name: str,
        point: Point
    ) -> float:
        raise Exception("Concrete classes derived from Expression must implement _numeric_partial()")

    @abstractmethod
    def _synthetic_partial(
        self: Expression,
        variable_name: str
    ) -> Expression:
        raise Exception("Concrete classes derived from Expression must implement _synthetic_partial()")

    def _numeric_partials(
        self: Expression,
        point: Point
    ) -> dict[str, float]:
        accumulator = acc.NumericPartialsAccumulator()
        self._reset_evaluation_cache()
        self._compute_numeric_partials(accumulator, 1, point)
        return accumulator.numeric_partials_for(self._variable_names)

    @abstractmethod
    def _compute_numeric_partials(
        self: Expression,
        accumulator: NumericPartialsAccumulator,
        multiplier: float,
        point: Point
    ) -> None: # instead of returning a value, we mutate the accumulator argument
        raise Exception("Concrete classes derived from Expression must implement _compute_numeric_partials()")

    def _synthetic_partials(
        self: Expression
    ) -> dict[str, Expression]:
        accumulator = acc.SyntheticPartialsAccumulator()
        self._compute_synthetic_partials(accumulator, ex.Constant(1))
        return accumulator.synthetic_partials_for(self._variable_names)

    @abstractmethod
    def _compute_synthetic_partials(
        self: Expression,
        accumulator: SyntheticPartialsAccumulator,
        multiplier: Expression
    ) -> None: # instead of returning a value, we mutate the accumulator argument
        raise Exception("Concrete classes derived from Expression must implement _compute_synthetic_partials()")

    ## Normalization and Reduction ##

    def _normalize(
        self: Expression
    ) -> Expression:
        """
        Reduces and normalizes an expression.
        """
        fully_reduced = self._fully_reduce()
        normalized = fully_reduced._normalize_fully_reduced()
        return normalized

    def _fully_reduce(
        self: Expression
    ) -> Expression:
        expression = self
        for _ in range(0, REDUCTION_STEPS_BOUND):
            if expression._is_fully_reduced:
                return expression
            expression = expression._take_reduction_step()
        logging.warning(f"Unable to fully reduce within {REDUCTION_STEPS_BOUND} steps")
        expression._is_fully_reduced = True
        return expression

    @abstractmethod
    def _take_reduction_step(
        self: Expression
    ) -> Expression:
        raise Exception("Concrete classes derived from Expression must implement _take_reduction_step()")

    def _consolidate_expression_lacking_variables(
        self: Expression
    ) -> Optional[Expression]:
        if self._variable_names:
            return None
        if isinstance(self, ex.Constant):
            return None
        if self._evaluation_failed:
            return None
        try:
            value = self.at(pt.Point())
            return ex.Constant(value)
        except er.DomainError:
            self._evaluation_failed = True
            return None

    @abstractmethod
    def _normalize_fully_reduced(
        self: Expression
    ) -> Expression:
        raise Exception("Concrete classes derived from Expression must implement _normalize_fully_reduced()")

    ## Operations ##

    def __neg__(
        self: Expression
    ) -> Negation:
        """Takes the negative of this expression."""
        return ex.Negation(self)

    def __add__(
        self: Expression,
        other: Expression
    ) -> Add:
        """Add this expression with another."""
        return ex.Add(self, other)

    def __sub__(
        self: Expression,
        other: Expression
    ) -> Minus:
        """Subtract another expression from this expression."""
        return ex.Minus(self, other)

    def __mul__(
        self: Expression,
        other: Expression
    ) -> Multiply:
        """Multiply this expression with another."""
        return ex.Multiply(self, other)

    def __truediv__(
        self: Expression,
        other: Expression
    ) -> Divide:
        """Divide this expression by another."""
        return ex.Divide(self, other)

    def __pow__(
        self: Expression,
        exponent: int | Expression
    ) -> NthPower | Power:
        """Raise this expression to an integer or another expression."""
        if isinstance(exponent, Expression):
            return ex.Power(self, exponent)
        # We want to accept a float representation of an integer (e.g. 3.0) even though
        # that wouldn't pass type checking.
        n = util.integer_from_integral_float(exponent)
        if isinstance(n, int):
            return ex.NthPower(self, n)
        raise Exception(f"Expected exponent to be an Expression or int, found: {exponent}")


def get_the_single_variable_name(
    expression: Expression,
    exception_message: str
) -> str:
    variable_names = expression._variable_names
    variable_names_count = len(variable_names)
    if variable_names_count == 1:
        (variable_name,) = variable_names
        return variable_name
    elif variable_names_count == 0:
        return "whatever"
    else:
        raise Exception(exception_message)


# The right slot of the returned tuple will have type expression_type
def first_of_given_type(
    expressions: list[Expression],
    expression_type: type
) -> Optional[tuple[int, Any]]:
    predicate = lambda expression: isinstance(expression, expression_type)
    return util.first_match_by_predicate(expressions, predicate)


# The left slot of the returned tuple will be all expressions with type expression_type
def partition_by_given_type(
    expressions: list[Expression],
    expression_type: type
) -> tuple[list[Any], list[Expression]]:
    predicate = lambda expression: isinstance(expression, expression_type)
    return util.partition_by_predicate(expressions, predicate)
