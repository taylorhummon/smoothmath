from typing import TYPE_CHECKING, Mapping
if TYPE_CHECKING:
    from src.reverse_accumulation.expression import Variable

type Real = float | int
type VariableValues = Mapping[Variable, Real]
