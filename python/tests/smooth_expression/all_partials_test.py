from src.smooth_expression.all_partials import AllPartials
from src.smooth_expression.variable import Variable

def testAllPartials():
    w = Variable("w")
    x = Variable("x")
    y = Variable("y")
    allPartials = AllPartials()
    allPartials._addSeed(x, 3)
    allPartials._addSeed(y, 4)
    allPartials._addSeed(y, 2)
    assert allPartials.partialWithRespectTo(w) == 0
    assert allPartials.partialWithRespectTo(x) == 3
    assert allPartials.partialWithRespectTo(y) == 6
