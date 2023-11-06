from src.smooth_expression.variable import Variable

def testVariable():
    x = Variable("x")
    singleResult = x.deriveSingle({ x: 2 }, x)
    assert singleResult.value == 2
    assert singleResult.partial == 1
    y = Variable("y")
    multiResult = x.deriveMulti({ x: 2, y: 3 })
    assert multiResult.value == 2
    assert multiResult.partialWithRespectTo(x) == 1
    assert multiResult.partialWithRespectTo(y) == 0
