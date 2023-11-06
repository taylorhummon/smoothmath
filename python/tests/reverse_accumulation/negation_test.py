from src.reverse_accumulation.constant import Constant
from src.reverse_accumulation.variable import Variable
from src.reverse_accumulation.negation import Negation

def testNegation():
    x = Variable("x")
    z = Negation(x)
    result = z.derive({ x: 2 })
    assert result.value == -2
    assert result.partialWithRespectTo(x) == -1

def testNegationComposition():
    x = Variable("x")
    z = Negation(Constant(2) * x + Constant(1))
    result = z.derive({ x: 3 })
    assert result.value == -7
    assert result.partialWithRespectTo(x) == -2
