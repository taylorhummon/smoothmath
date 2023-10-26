from src.forward_accumulation.custom_types import numeric

class ValueAndPartial:
    def __init__(self, value: numeric, partial: numeric):
        self.value = value
        self.partial = partial

    def toPair(self) -> tuple[numeric, numeric]:
        return (self.value, self.partial)
