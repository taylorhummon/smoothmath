from src.smooth_expression.constant import Constant
from src.smooth_expression.variable import Variable

def testConstant():
    c = Constant(7)
    assert c.evaluate({}) == 7
    x = Variable("x")
    partial = c.partialAt({ x: 2 }, x)
    assert partial == 0
    allPartials = c.allPartialsAt({ x: 2 })
    assert allPartials.partialWithRespectTo(x) == 0
