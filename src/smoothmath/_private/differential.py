from __future__ import annotations
from typing import TYPE_CHECKING, Any
import smoothmath._private.partial as pa
import smoothmath._private.located_differential as ld
import smoothmath._private.utilities as util
if TYPE_CHECKING:
    from smoothmath import RealNumber, Point, Expression, Partial, LocatedDifferential
    from smoothmath.expression import Variable


class Differential:
    """
    The differential of an expression.

    :param expression: an expression
    """

    def __init__(
        self: Differential,
        expression: Expression
    ) -> None:
        self._original_expression: Expression
        self._original_expression = expression
        self._synthetic_partials: dict[str, Expression]
        self._synthetic_partials = _retrieve_normalized_synthetic_partials(expression)

    def component_at(
        self: Differential,
        variable: Variable | str,
        point: Point
    ) -> RealNumber:
        """
        The component of the differential localized at a point.

        :param point: where to localize
        :param variable: selects which component
        """
        return self.component(variable).at(point)

    def component(
        self: Differential,
        variable: Variable | str
    ) -> Partial:
        """
        The component of the differential.

        :param variable: selects which component
        """
        variable_name = util.get_variable_name(variable)
        synthetic_partial = self._synthetic_partials.get(variable_name, None)
        return pa.Partial(
            self._original_expression,
            variable_name,
            synthetic_partial = synthetic_partial
        )

    def at(
        self: Differential,
        point: Point
    ) -> LocatedDifferential:
        """
        Localize the differential at a point.

        :param point: where to localize
        """
        self._original_expression.evaluate(point)
        numeric_partials: dict[str, RealNumber]
        numeric_partials = {}
        for variable_name, synthetic_partial in self._synthetic_partials.items():
            numeric_partials[variable_name] = synthetic_partial.evaluate(point)
        return ld.LocatedDifferential(self._original_expression, point, numeric_partials)

    def __eq__(
        self: Differential,
        other: Any
    ) -> bool:
        return (
            (other.__class__ == self.__class__) and
            (self._original_expression == other._original_expression) and
            (self._synthetic_partials == other._synthetic_partials)
        )

    def __hash__(
        self: Differential
    ) -> int:
        data = tuple(sorted(self._synthetic_partials.items()))
        return hash((self._original_expression, data))

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


def _retrieve_normalized_synthetic_partials(
    original_expression: Expression
) -> dict[str, Expression]:
    return util.map_dictionary_values(
        original_expression._synthetic_partials(),
        lambda _, synthetic_partial: synthetic_partial._normalize()
    )
