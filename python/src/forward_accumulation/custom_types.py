from typing import TYPE_CHECKING, Mapping
if TYPE_CHECKING:
    from src.forward_accumulation.expression import Variable

type numeric = float | int
type VariableValues = Mapping[Variable, numeric]
