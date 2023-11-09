from src.smooth_expression.variable import Variable

def testVariable():
    x = Variable("x")
    value = x.evaluate({ x: 2 })
    assert value == 2
    partial = x.partialAt({ x: 2 }, x)
    assert partial == 1
    y = Variable("y")
    allPartials = x.allPartialsAt({ x: 2, y: 3 })
    assert allPartials.partialWithRespectTo(x) == 1
    assert allPartials.partialWithRespectTo(y) == 0
