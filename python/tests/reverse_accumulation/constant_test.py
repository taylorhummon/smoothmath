from src.reverse_accumulation.constant import Constant
from src.reverse_accumulation.variable import Variable

def testConstant():
    c = Constant(7)
    x = Variable("x")
    result = c.derive({ x: 2 })
    assert result.value == 7
    assert result.partialWithRespectTo(x) == 0
