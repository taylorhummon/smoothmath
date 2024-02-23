from __future__ import annotations
from typing import TYPE_CHECKING, Any, Optional
import smoothmath._private.partial as pa
import smoothmath._private.located_differential as ld
import smoothmath._private.expression.variable as va
import smoothmath._private.utilities as util
if TYPE_CHECKING:
    from smoothmath import Point, Expression, Partial, LocatedDifferential
    from smoothmath.expression import Variable


class Differential:
    """
    The differential of an expression.

    >>> from smoothmath import Differential
    >>> from smoothmath.expression import Variable, Multiply
    >>> Differential(Multiply(Variable("x"), Variable("y")))
    Differential(Multiply(Variable("x"), Variable("y")))

    :param expression: an expression
    :param compute_early: whether to do extra work on initialization to have faster evaluation afterwards
    """

    def __init__(
        self: Differential,
        expression: Expression,
        compute_early: bool = False
    ) -> None:
        self._original_expression: Expression
        self._original_expression = expression
        self._synthetic_partials: Optional[dict[str, Expression]]
        self._synthetic_partials = _initial_synthetic_partials(expression, compute_early)

    def component(
        self: Differential,
        variable: Variable | str
    ) -> Partial:
        """
        Retrieves a component of the differential.

        NOTE: The components of the differential are the partials of the original expression.

        :param variable: selects which component
        """
        if self._synthetic_partials is None:
            return pa.Partial(self._original_expression, variable)
        variable_name = va.get_variable_name(variable)
        synthetic_partial = self._synthetic_partials.get(variable_name, None)
        if synthetic_partial is None:
            return pa.Partial(self._original_expression, variable)
        _private = { "synthetic_partial": synthetic_partial }
        return pa.Partial(self._original_expression, variable, _private = _private)

    def at(
        self: Differential,
        point: Point
    ) -> LocatedDifferential:
        """
        Evaluates the differential at a point.

        :param point: where to evaluate
        """
        self._original_expression.at(point)
        if self._synthetic_partials is None:
            return ld.LocatedDifferential(self._original_expression, point)
        numeric_partials = util.map_dictionary_values(
            self._synthetic_partials,
            lambda _, synthetic_partial: synthetic_partial.at(point)
        )
        _private = { "numeric_partials": numeric_partials }
        return ld.LocatedDifferential(self._original_expression, point, _private = _private)

    def component_at(
        self: Differential,
        variable: Variable | str,
        point: Point
    ) -> float:
        """
        Retrieves a component of the differential and evaluates it at a point.

        :param variable: selects which component
        :param point: where to evaluate
        """
        return self.component(variable).at(point)

    def __eq__(
        self: Differential,
        other: Any
    ) -> bool:
        return (
            (other.__class__ == self.__class__) and
            (self._original_expression == other._original_expression)
        )

    def __hash__(
        self: Differential
    ) -> int:
        return hash(("Differential", self._original_expression))

    def __str__(
        self: Differential
    ) -> str:
        return self._to_string()

    def __repr__(
        self: Differential
    ) -> str:
        return self._to_string()

    def _to_string(
        self: Differential
    ) -> str:
        return f"Differential({self._original_expression})"


def _initial_synthetic_partials(
    original_expression: Expression,
    compute_early: bool
) -> Optional[dict[str, Expression]]:
    if compute_early:
        synthetic_partials = original_expression._synthetic_partials()
        return util.map_dictionary_values(
            synthetic_partials,
            lambda _, synthetic_partial: synthetic_partial._normalize()
        )
    else:
        return None
