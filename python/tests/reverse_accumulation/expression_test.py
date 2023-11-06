from pytest import approx, raises
from src.reverse_accumulation.custom_exceptions import DomainException
from src.reverse_accumulation.constant import Constant
from src.reverse_accumulation.variable import Variable
from src.reverse_accumulation.exponential import Exponential

def testPolynomialOfOneVariable():
    x = Variable("x")
    z = x * x - Constant(6) * x + Constant(4)
    result = z.derive({ x: 2 })
    assert result.value == -4
    assert result.partialWithRespectTo(x) == -2

def testPolynomialOfTwoVariables():
    x = Variable("x")
    y = Variable("y")
    z = x * (x + y) - Constant(5) * y * y
    result = z.derive({ x: 2, y: 3 })
    assert result.value == -35
    assert result.partialWithRespectTo(x) == 7
    assert result.partialWithRespectTo(y) == -28

def testPolynomialOfThreeVariables():
    w = Variable("w")
    x = Variable("x")
    y = Variable("y")
    z = w * w + Constant(5) * w * x * x - w * x * y
    result = z.derive({ w: 2, x: 3, y: 4 })
    assert result.value == 70
    assert result.partialWithRespectTo(w) == 37
    assert result.partialWithRespectTo(x) == 52
    assert result.partialWithRespectTo(y) == -6

def testUnrelatedVariable():
    x = Variable("x")
    y = Variable("y")
    z = x ** Constant(2)
    result = z.derive({ x: 2 })
    assert result.value == 4
    assert result.partialWithRespectTo(y) == 0

def testCompositeFunction():
    x = Variable("x")
    z = Exponential(x ** Constant(2))
    result = z.derive({ x: 2 })
    assert result.value == approx(54.598150033)
    assert result.partialWithRespectTo(x) == approx(218.392600132)

def testIndeterminateForm():
    t = Variable("t")
    z = (Constant(2) * t) / t
    with raises(DomainException):
        z.derive({ t: 0 })

def testExpressionReuse():
    x = Variable("x")
    w = x ** Constant(2)
    z = (w + Constant(1)) / w
    result = z.derive({ x: 2 })
    assert result.value == approx(1.25)
    assert result.partialWithRespectTo(x) == approx(-0.25)
