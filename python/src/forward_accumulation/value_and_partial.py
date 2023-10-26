from __future__ import annotations
from src.forward_accumulation.custom_types import numeric

class ValueAndPartial:
    def __init__(
        self: ValueAndPartial,
        value: numeric,
        partial: numeric
    ):
        self.value = value
        self.partial = partial

    def toPair(
        self: ValueAndPartial
    ) -> tuple[numeric, numeric]:
        return (self.value, self.partial)
