from pytest import approx, raises
import math
from src.reverse_accumulation.custom_exceptions import DomainException
from src.reverse_accumulation.constant import Constant
from src.reverse_accumulation.variable import Variable
from src.reverse_accumulation.square_root import SquareRoot

def testSquareRoot():
    x = Variable("x")
    z = SquareRoot(x)
    result = z.derive({ x: 4 })
    assert result.value == approx(2)
    assert result.partialWithRespectTo(x) == approx(0.25)
    with raises(DomainException):
        z.derive({ x: 0 })
    with raises(DomainException):
        z.derive({ x: -1 })

def testSquareRootComposition():
    x = Variable("x")
    z = SquareRoot(Constant(2) * x + Constant(7))
    result = z.derive({ x: 1 })
    assert result.value == approx(3)
    assert result.partialWithRespectTo(x) == approx(1 / 3)
