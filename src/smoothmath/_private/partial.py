from __future__ import annotations
from typing import TYPE_CHECKING, Any, Optional
import smoothmath._private.expression.variable as va
if TYPE_CHECKING:
    from smoothmath import Point, Expression
    from smoothmath.expression import Variable


class Partial:
    """
    The partial derivative of an expression.

    >>> from smoothmath import Partial
    >>> from smoothmath.expression import Variable, Multiply
    >>> Partial(Multiply(Variable("x"), Variable("y")), Variable("x"))
    Partial(Multiply(Variable("x"), Variable("y")), Variable("x"))

    :param expression: an expression
    :param variable: the partial is taken with respect to this variable
    :param compute_early: whether to do extra work on initialization to have faster evaluation afterwards
    """

    def __init__(
        self: Partial,
        expression: Expression,
        variable: Variable | str,
        compute_early: bool = False,
        _private: Optional[dict[str, Expression]] = None
    ) -> None:
        variable_name = va.get_variable_name(variable)
        self._original_expression: Expression
        self._original_expression = expression
        self._variable_name: str
        self._variable_name = variable_name
        self._synthetic_partial: Optional[Expression]
        self._synthetic_partial = _initial_synthetic_partial(
            expression, variable_name, compute_early, _private
        )

    def at(
        self: Partial,
        point: Point
    ) -> float:
        """
        Evaluates the partial at a point.

        :param point: where to evaluate the partial
        """
        if self._synthetic_partial is None:
            self._original_expression._reset_evaluation_cache()
            return self._original_expression._numeric_partial(self._variable_name, point)
        else:
            # We evaluate the original expression to check for DomainErrors.
            self._original_expression.at(point)
            return self._synthetic_partial.at(point)

    def as_expression(
        self: Partial
    ) -> Expression:
        """
        Writes the partial as an expression.

        NOTE: Writing the partial as an expression may enlargen the domain. For example,
        ``Partial(Logarithm(Variable("x")), Variable("x"))`` is not defined at negative numbers,
        but as an expression, ``Reciprocal(Variable("x"))`` is defined at negative numbers.
        """
        if self._synthetic_partial is None:
            self._synthetic_partial = _retrieve_synthetic_partial(
                self._original_expression,
                self._variable_name
            )
        return self._synthetic_partial

    def __eq__(
        self: Partial,
        other: Any
    ) -> bool:
        return (
            (other.__class__ == self.__class__) and
            (self._original_expression == other._original_expression) and
            (self._variable_name == other._variable_name)
        )

    def __hash__(
        self: Partial
    ) -> int:
        return hash(("Partial", self._original_expression))

    def __str__(
        self: Partial
    ) -> str:
        return self._to_string()

    def __repr__(
        self: Partial
    ) -> str:
        return self._to_string()

    def _to_string(
        self: Partial
    ) -> str:
        variable_string = f"Variable(\"{self._variable_name}\")"
        return f"Partial({self._original_expression}, {variable_string})"


def _initial_synthetic_partial(
    original_expression: Expression,
    variable_name: str,
    compute_eagly: bool,
    _private: Optional[dict[str, Expression]]
) -> Optional[Expression]:
    if _private is not None and "synthetic_partial" in _private:
        # We'll assume that if a synthetic partial was passed in to the constructor,
        # we don't need to normalize it.
        return _private["synthetic_partial"]
    elif compute_eagly:
        return _retrieve_synthetic_partial(original_expression, variable_name)
    else:
        return None


def _retrieve_synthetic_partial(
    original_expression: Expression,
    variable_name: str
) -> Expression:
    return original_expression._synthetic_partial(variable_name)._normalize()
