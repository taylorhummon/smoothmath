from src.smooth_expression.constant import Constant
from src.smooth_expression.variable import Variable

def testConstant():
    c = Constant(7)
    assert c.evaluate({}) == 7
    x = Variable("x")
    singleResult = c.deriveSingle({ x: 2 }, x)
    assert singleResult.value == 7
    assert singleResult.partial == 0
    multiResult = c.deriveMulti({ x: 2 })
    assert multiResult.value == 7
    assert multiResult.partialWithRespectTo(x) == 0
