from src.forward_accumulation.constant import Constant
from src.forward_accumulation.variable import Variable
from src.forward_accumulation.negation import Negation

def testNegation():
    x = Variable("x")
    z = Negation(x)
    result = z.derive({ x: 2 }, x)
    assert result.value == -2
    assert result.partial == -1

def testNegationComposition():
    x = Variable("x")
    z = Negation(Constant(2) * x + Constant(1))
    result = z.derive({ x: 3 }, x)
    assert result.value == -7
    assert result.partial == -2
