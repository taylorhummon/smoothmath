from pytest import approx, raises
from src.smooth_expression.custom_exceptions import DomainException
from src.smooth_expression.constant import Constant
from src.smooth_expression.variable import Variable
from src.smooth_expression.square_root import SquareRoot

def testSquareRoot():
    x = Variable("x")
    z = SquareRoot(x)
    partial = z.deriveSingle({ x: 4 }, x)
    assert partial == approx(0.25)
    with raises(DomainException):
        z.deriveSingle({ x: 0 }, x)
    with raises(DomainException):
        z.deriveSingle({ x: -1 }, x)

def testSquareRootComposition():
    x = Variable("x")
    z = SquareRoot(Constant(2) * x + Constant(7))
    partial = z.deriveSingle({ x: 1 }, x)
    assert partial == approx(1 / 3)

def testSquareRootMulti():
    x = Variable("x")
    z = SquareRoot(x)
    multiResult = z.deriveMulti({ x: 4 })
    assert multiResult.value == approx(2)
    assert multiResult.partialWithRespectTo(x) == approx(0.25)
    with raises(DomainException):
        z.deriveMulti({ x: 0 })
    with raises(DomainException):
        z.deriveMulti({ x: -1 })

def testSquareRootCompositionMulti():
    x = Variable("x")
    z = SquareRoot(Constant(2) * x + Constant(7))
    multiResult = z.deriveMulti({ x: 1 })
    assert multiResult.value == approx(3)
    assert multiResult.partialWithRespectTo(x) == approx(1 / 3)
