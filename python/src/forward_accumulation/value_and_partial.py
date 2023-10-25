class ValueAndPartial:
    def __init__(self, value, partial):
        self.value = value
        self.partial = partial

    def toList(self):
        return [self.value, self.partial]
