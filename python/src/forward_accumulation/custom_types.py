from typing import TYPE_CHECKING, Mapping
if TYPE_CHECKING:
    from src.forward_accumulation.variable import Variable

type Real = float | int
type VariableValues = Mapping[Variable, Real]
