from pytest import approx
from src.reverse_accumulation.constant import Constant
from src.reverse_accumulation.variable import Variable
from src.reverse_accumulation.minus import Minus

def testMinus():
    x = Variable("x")
    y = Variable("y")
    z = Minus(x, y)
    result = z.derive({ x: 2, y: 3 })
    assert result.value == approx(-1)
    assert result.partialWithRespectTo(x) == approx(1)
    assert result.partialWithRespectTo(y) == approx(-1)

def testMinusComposition():
    x = Variable("x")
    y = Variable("y")
    z = Minus(Constant(5) * x, Constant(4) * y)
    result = z.derive({ x: 2, y: 3 })
    assert result.value == approx(-2)
    assert result.partialWithRespectTo(x) == approx(5)
    assert result.partialWithRespectTo(y) == approx(-4)
