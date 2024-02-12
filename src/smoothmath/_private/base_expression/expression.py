from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from abc import ABC, abstractmethod
import logging
import smoothmath._private.expression as ex
import smoothmath._private.errors as er
import smoothmath._private.point as pt
import smoothmath._private.global_partial as gp
import smoothmath._private.local_differential as ld
import smoothmath._private.global_differential as gd
import smoothmath._private.utilities as util
if TYPE_CHECKING:
    from smoothmath import RealNumber, Point, GlobalDifferential, LocalDifferential, GlobalPartial
    from smoothmath.expression import (
        Variable, Add, Minus, Negation, Multiply, Divide, Power, NthPower
    )
    from smoothmath._private.local_differential import LocalDifferentialBuilder
    from smoothmath._private.global_differential import GlobalDifferentialBuilder


REDUCTION_STEPS_BOUND = 1000


class Expression(ABC):
    def __init__(
        self: Expression,
        lacks_variables: bool
    ) -> None:
        self._lacks_variables: bool
        self._lacks_variables = lacks_variables
        self._is_fully_reduced: bool
        self._is_fully_reduced = False

    ## Evaluation ##

    def evaluate(
        self: Expression,
        point: Point
    ) -> RealNumber:
        """
        Evaluates the expression.

        :param point: where to evaluate
        """
        if not isinstance(point, pt.Point):
            raise Exception("Must provide a Point to evaluate()")
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
    ) -> RealNumber:
        raise Exception("Concrete classes derived from Expression must implement _evaluate()")

    ## Partials and Differentials ##

    def local_partial(
        self: Expression,
        point: Point,
        variable: Variable | str
    ) -> RealNumber:
        """
        Takes the partial derivative of the expression and localizes at a point.

        :param point: where to localize
        :param variable: the partial is taken with respect to this variable
        """
        if not isinstance(point, pt.Point):
            raise Exception("Must provide a Point to local_partial()")
        self._reset_evaluation_cache()
        variable_name = util.get_variable_name(variable)
        return self._local_partial(point, variable_name)

    @abstractmethod
    def _local_partial(
        self: Expression,
        point: Point,
        variable_name: str
    ) -> RealNumber:
        raise Exception("Concrete classes derived from Expression must implement _local_partial()")

    def global_partial(
        self: Expression,
        variable: Variable | str
    ) -> GlobalPartial:
        """
        Takes the partial derivative of the expression.

        :param variable: the partial is taken with respect to this variable
        """
        variable_name = util.get_variable_name(variable)
        synthetic_partial = self._synthetic_partial(variable_name)
        return gp.GlobalPartial.build(self, synthetic_partial)

    @abstractmethod
    def _synthetic_partial(
        self: Expression,
        variable_name: str
    ) -> Expression:
        raise Exception("Concrete classes derived from Expression must implement _synthetic_partial()")

    def local_differential(
        self: Expression,
        point: Point
    ) -> LocalDifferential:
        """
        Takes the differential of the expression and localizes at a point.

        :param point: where to localize
        """
        if not isinstance(point, pt.Point):
            raise Exception("Must provide a Point to local_differential()")
        self._reset_evaluation_cache()
        builder = ld.LocalDifferentialBuilder(self, point)
        self._compute_local_differential(builder, 1)
        return builder.build()

    @abstractmethod
    def _compute_local_differential(
        self: Expression,
        builder: LocalDifferentialBuilder,
        accumulated: RealNumber
    ) -> None: # instead of returning a value, we mutate the local_differential argument
        raise Exception("Concrete classes derived from Expression must implement _compute_local_differential()")

    def global_differential(
        self: Expression
    ) -> GlobalDifferential:
        """
        Takes the differential of the expression.
        """
        builder = gd.GlobalDifferentialBuilder(self)
        self._compute_global_differential(builder, ex.Constant(1))
        return builder.build()

    @abstractmethod
    def _compute_global_differential(
        self: Expression,
        builder: GlobalDifferentialBuilder,
        accumulated: Expression
    ) -> None: # instead of returning a value, we mutate the global_differential argument
        raise Exception("Concrete classes derived from Expression must implement _compute_global_differential()")

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
        if self._lacks_variables and not isinstance(self, ex.Constant):
            try:
                value = self.evaluate(pt.Point())
                return ex.Constant(value)
            except er.DomainError:
                self._lacks_variables = False # PERFORMANCE HACK: don't retry evaluation
                return None
        else:
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
        n = util.integer_from_integral_real_number(exponent)
        if isinstance(n, int):
            return ex.NthPower(self, n)
        raise Exception(f"Expected exponent to be an Expression or int, found: {exponent}")
