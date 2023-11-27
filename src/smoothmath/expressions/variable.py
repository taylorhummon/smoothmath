from __future__ import annotations
from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:
    from smoothmath.types import real_number
    from smoothmath.point import Point
    from smoothmath.all_partials import AllPartials
    from smoothmath.synthetic import Synthetic
    from smoothmath.expression import Expression

from smoothmath.expression import NullaryExpression
import smoothmath.expressions as ex


class Variable(NullaryExpression):
    def __init__(
        self: Variable,
        name: str
    ) -> None:
        super().__init__(lacks_variables = False)
        if not name:
            raise Exception("Variables must be given a non-blank name")
        self.name: str
        self.name = name
        self._cached_hash: int | None
        self._cached_hash = None

    def __eq__(
        self: Variable,
        other: Any
    ) -> bool:
        return isinstance(other, Variable) and (other.name == self.name)

    def __hash__(
        self: Variable
    ) -> int:
        if self._cached_hash is None:
            self._cached_hash = hash(self.name)
        return self._cached_hash

    def __str__(
        self: Variable
    ) -> str:
        return f"Variable(\"{self.name}\")"

    def _evaluate(
        self: Variable,
        point: Point
    ) -> real_number:
        return point.value_for(self.name)

    def _partial_at(
        self: Variable,
        point: Point,
        with_respect_to: str
    ) -> real_number:
        if self.name == with_respect_to:
            return 1
        else:
            return 0

    def _compute_all_partials_at(
        self: Variable,
        all_partials: AllPartials,
        point: Point,
        accumulated: real_number
    ) -> None:
        all_partials._add_to(self, accumulated)

    def _synthetic_partial(
        self: Variable,
        with_respect_to: str
    ) -> Expression:
        if self.name == with_respect_to:
            return ex.Constant(1)
        else:
            return ex.Constant(0)

    def _compute_all_synthetic_partials(
        self: Variable,
        synthetic: Synthetic,
        accumulated: Expression
    ) -> None:
        synthetic._add_to(self, accumulated)
