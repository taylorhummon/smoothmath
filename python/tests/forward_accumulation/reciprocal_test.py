from pytest import approx, raises
from src.forward_accumulation.custom_exceptions import DomainException
from src.forward_accumulation.constant import Constant
from src.forward_accumulation.variable import Variable
from src.forward_accumulation.reciprocal import Reciprocal

def testReciprocal():
    x = Variable("x")
    z = Reciprocal(x)
    result = z.derive({ x: 2 }, x)
    assert result.value == approx(0.5)
    assert result.partial == approx(-0.25)
    with raises(DomainException):
        z.derive({ x: 0 }, x)
    result = z.derive({ x: -1 }, x)
    assert result.value == approx(-1)
    assert result.partial == approx(-1)

def testReciprocalComposition():
    x = Variable("x")
    z = Reciprocal(Constant(2) * x - Constant(4))
    result = z.derive({ x: 3 }, x)
    assert result.value == approx(0.5)
    assert result.partial == approx(-0.5)
