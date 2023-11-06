from pytest import approx, raises
from src.forward_accumulation.custom_exceptions import DomainException
from src.forward_accumulation.constant import Constant
from src.forward_accumulation.variable import Variable
from src.forward_accumulation.exponential import Exponential

def testPolynomialOfOneVariable():
    x = Variable("x")
    z = x * x - Constant(6) * x + Constant(4)
    result = z.derive({ x: 2 }, x)
    assert result.value == -4
    assert result.partial == -2

def testPolynomialOfTwoVariables():
    x = Variable("x")
    y = Variable("y")
    z = x * (x + y) - Constant(5) * y * y
    variableValues = { x: 2, y: 3 }
    resultForX = z.derive(variableValues, x)
    assert resultForX.value == -35
    assert resultForX.partial == 7
    resultForY = z.derive(variableValues, y)
    assert resultForY.value == -35
    assert resultForY.partial == -28

def testPolynomialOfThreeVariables():
    w = Variable("w")
    x = Variable("x")
    y = Variable("y")
    z = w * w + Constant(5) * w * x * x - w * x * y
    variableValues = { w: 2, x: 3, y: 4 }
    resultForW = z.derive(variableValues, w)
    assert resultForW.value == 70
    assert resultForW.partial == 37
    resultForX = z.derive(variableValues, x)
    assert resultForX.value == 70
    assert resultForX.partial == 52
    resultForY = z.derive(variableValues, y)
    assert resultForY.value == 70
    assert resultForY.partial == -6

def testUnrelatedVariable():
    x = Variable("x")
    y = Variable("y")
    z = x ** Constant(2)
    result = z.derive({ x: 2 }, y)
    assert result.value == 4
    assert result.partial == 0

def testCompositeFunction():
    x = Variable("x")
    z = Exponential(x ** Constant(2))
    result = z.derive({ x: 2 }, x)
    assert result.value == approx(54.598150033)
    assert result.partial == approx(218.392600132)

def testIndeterminateForm():
    t = Variable("t")
    z = (Constant(2) * t) / t
    with raises(DomainException):
        z.derive({ t: 0 }, t)

def testExpressionReuse():
    x = Variable("x")
    w = x ** Constant(2)
    z = (w + Constant(1)) / w
    result = z.derive({ x: 2 }, x)
    assert result.value == approx(1.25)
    assert result.partial == approx(-0.25)
