from __future__ import annotations
from typing import TYPE_CHECKING, Any, Optional
import smoothmath._private.partial as pa
import smoothmath._private.located_differential as ld
import smoothmath._private.expression.variable as va
import smoothmath._private.utilities as util
if TYPE_CHECKING:
    from smoothmath import RealNumber, Point, Expression, Partial, LocatedDifferential
    from smoothmath.expression import Variable


class Differential:
    """
    The differential of an expression.

    :param expression: an expression
    :param compute_eagerly: whether to do extra work on initialization to have faster evaluation afterwards
    """

    def __init__(
        self: Differential,
        expression: Expression,
        compute_eagerly: bool = False
    ) -> None:
        self._original_expression: Expression
        self._original_expression = expression
        self._synthetic_partials: Optional[dict[str, Expression]]
        self._synthetic_partials = _initial_synthetic_partials(expression, compute_eagerly)

    def part(
        self: Differential,
        variable: Variable | str
    ) -> Partial:
        """
        Retrieves a part of the differential.

        NOTE: The parts of the differential are the partials of the original expression.

        :param variable: selects which part
        """
        return pa.Partial(
            self._original_expression,
            variable,
            synthetic_partial = _synthetic_partial_from(self._synthetic_partials, variable)
        )

    def at(
        self: Differential,
        point: Point
    ) -> LocatedDifferential:
        """
        Evaluates the differential at a point.

        :param point: where to evaluate
        """
        self._original_expression.at(point)
        return ld.LocatedDifferential(
            self._original_expression,
            point,
            numeric_partials = _numeric_partials_from(self._synthetic_partials, point)
        )

    def part_at(
        self: Differential,
        variable: Variable | str,
        point: Point
    ) -> RealNumber:
        """
        Retrievs a part of the differential and evaluates it at a point.

        :param variable: selects which part
        :param point: where to evaluate
        """
        return self.part(variable).at(point)

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
    compute_eagerly: bool
) -> Optional[dict[str, Expression]]:
    if compute_eagerly:
        synthetic_partials = original_expression._synthetic_partials()
        return util.map_dictionary_values(
            synthetic_partials,
            lambda _, synthetic_partial: synthetic_partial._normalize()
        )
    else:
        return None


def _synthetic_partial_from(
    synthetic_partials: Optional[dict[str, Expression]],
    variable: Variable | str
) -> Optional[Expression]:
    if synthetic_partials is None:
        return None
    else:
        variable_name = va.get_variable_name(variable)
        return synthetic_partials.get(variable_name, None)


def _numeric_partials_from(
    synthetic_partials: Optional[dict[str, Expression]],
    point: Point
) -> Optional[dict[str, RealNumber]]:
    if synthetic_partials is None:
        return None
    else:
        return util.map_dictionary_values(
            synthetic_partials,
            lambda _, synthetic_partial: synthetic_partial.at(point)
        )
