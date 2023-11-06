from src.forward_accumulation.constant import Constant
from src.forward_accumulation.variable import Variable

def testConstant():
    c = Constant(7)
    assert c.value == 7
    x = Variable("x")
    result = c.derive({ x: 2 }, x)
    assert result.value == 7
    assert result.partial == 0
