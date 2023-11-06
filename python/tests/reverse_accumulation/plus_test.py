from pytest import approx, raises
from src.reverse_accumulation.constant import Constant
from src.reverse_accumulation.variable import Variable
from src.reverse_accumulation.plus import Plus

def testPlus():
    x = Variable("x")
    y = Variable("y")
    z = Plus(x, y)
    result = z.derive({ x: 2, y: 3 })
    assert result.value == approx(5)
    assert result.partialWithRespectTo(x) == approx(1)
    assert result.partialWithRespectTo(y) == approx(1)

def testPlusComposition():
    x = Variable("x")
    y = Variable("y")
    z = Plus(Constant(5) * x, Constant(4) * y)
    result = z.derive({ x: 2, y: 3 })
    assert result.value == approx(22)
    assert result.partialWithRespectTo(x) == approx(5)
    assert result.partialWithRespectTo(y) == approx(4)
