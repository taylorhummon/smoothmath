from src.forward_accumulation.variable import Variable

def testVariable():
    x = Variable("x")
    result = x.derive({ x: 2 }, x)
    assert result.value == 2
    assert result.partial == 1
