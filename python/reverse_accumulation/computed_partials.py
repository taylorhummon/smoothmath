class ComputedPartials:
    def __init__(self):
        self._dict = {}

    def partialWithRespectTo(self, variable):
        return self._dict.get(variable, 0)

    def addSeed(self, variable, seed):
        self._dict[variable] = seed + self._dict.get(variable, 0)
