from pytest import approx, raises
from src.reverse_accumulation.custom_exceptions import DomainException
from src.reverse_accumulation.constant import Constant
from src.reverse_accumulation.variable import Variable
from src.reverse_accumulation.reciprocal import Reciprocal

def testReciprocal():
    x = Variable("x")
    z = Reciprocal(x)
    result = z.derive({ x: 2 })
    assert result.value == approx(0.5)
    assert result.partialWithRespectTo(x) == approx(-0.25)
    with raises(DomainException):
        z.derive({ x: 0 })
    result = z.derive({ x: -1 })
    assert result.value == approx(-1)
    assert result.partialWithRespectTo(x) == approx(-1)

def testReciprocalComposition():
    x = Variable("x")
    z = Reciprocal(Constant(2) * x - Constant(4))
    result = z.derive({ x: 3 })
    assert result.value == approx(0.5)
    assert result.partialWithRespectTo(x) == approx(-0.5)
