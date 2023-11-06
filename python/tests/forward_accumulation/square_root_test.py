from pytest import approx, raises
from src.forward_accumulation.custom_exceptions import DomainException
from src.forward_accumulation.constant import Constant
from src.forward_accumulation.variable import Variable
from src.forward_accumulation.square_root import SquareRoot

def testSquareRoot():
    x = Variable("x")
    z = SquareRoot(x)
    result = z.derive({ x: 4 }, x)
    assert result.value == approx(2)
    assert result.partial == approx(0.25)
    with raises(DomainException):
        z.derive({ x: 0 }, x)
    with raises(DomainException):
        z.derive({ x: -1 }, x)

def testSquareRootComposition():
    x = Variable("x")
    z = SquareRoot(Constant(2) * x + Constant(7))
    result = z.derive({ x: 1 }, x)
    assert result.value == approx(3)
    assert result.partial == approx(1 / 3)
