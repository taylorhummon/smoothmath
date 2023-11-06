from src.reverse_accumulation.variable import Variable

def testVariable():
    x = Variable("x")
    y = Variable("y")
    result = x.derive({ x: 2, y: 3 })
    assert result.value == 2
    assert result.partialWithRespectTo(x) == 1
    assert result.partialWithRespectTo(y) == 0
