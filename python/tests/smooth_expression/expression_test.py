from pytest import approx, raises
from src.smooth_expression.custom_exceptions import DomainException
from src.smooth_expression.variable_values import VariableValues
from src.smooth_expression.constant import Constant
from src.smooth_expression.variable import Variable
from src.smooth_expression.exponential import Exponential

def testPolynomialOfOneVariable():
    x = Variable("x")
    z = x * x - Constant(6) * x + Constant(4)
    variableValues = VariableValues({ x: 2 })
    value = z.evaluate(variableValues)
    assert value == -4
    partial = z.partialAt(variableValues, x)
    assert partial == -2
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == -2

def testPolynomialOfTwoVariables():
    x = Variable("x")
    y = Variable("y")
    z = x * (x + y) - Constant(5) * y * y
    variableValues = VariableValues({ x: 2, y: 3 })
    value = z.evaluate(variableValues)
    assert value == -35
    partialWithRespectToX = z.partialAt(variableValues, x)
    assert partialWithRespectToX == 7
    partialWithRespectToY = z.partialAt(variableValues, y)
    assert partialWithRespectToY == -28
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == 7
    assert allPartials.partialWithRespectTo(y) == -28

def testPolynomialOfThreeVariables():
    w = Variable("w")
    x = Variable("x")
    y = Variable("y")
    z = w * w + Constant(5) * w * x * x - w * x * y
    variableValues = VariableValues({ w: 2, x: 3, y: 4 })
    value = z.evaluate(variableValues)
    assert value == 70
    partialWithRespectToW = z.partialAt(variableValues, w)
    assert partialWithRespectToW == 37
    partialWithRespectToX = z.partialAt(variableValues, x)
    assert partialWithRespectToX == 52
    partialWithRespectToY = z.partialAt(variableValues, y)
    assert partialWithRespectToY == -6
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(w) == 37
    assert allPartials.partialWithRespectTo(x) == 52
    assert allPartials.partialWithRespectTo(y) == -6

def testUnrelatedVariable():
    x = Variable("x")
    y = Variable("y")
    z = x ** Constant(2)
    variableValues = VariableValues({ x: 2 })
    value = z.evaluate(variableValues)
    assert value == 4
    partial = z.partialAt(variableValues, y)
    assert partial == 0
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(y) == 0

def testCompositeFunction():
    x = Variable("x")
    z = Exponential(x ** Constant(2))
    variableValues = VariableValues({ x: 2 })
    value = z.evaluate(variableValues)
    assert value == approx(54.598150033)
    partial = z.partialAt(variableValues, x)
    assert partial == approx(218.392600132)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == approx(218.392600132)

def testIndeterminateForm():
    t = Variable("t")
    z = (Constant(2) * t) / t
    variableValues = VariableValues({ t: 0 })
    with raises(DomainException):
        z.evaluate(variableValues)
    with raises(DomainException):
        z.partialAt(variableValues, t)
    with raises(DomainException):
        z.allPartialsAt(variableValues)

def testExpressionReuse():
    x = Variable("x")
    w = x ** Constant(2)
    z = (w + Constant(1)) / w
    variableValues = VariableValues({ x: 2 })
    value = z.evaluate(variableValues)
    assert value == approx(1.25)
    partial = z.partialAt(variableValues, x)
    assert partial == approx(-0.25)
    allPartials = z.allPartialsAt(variableValues)
    assert allPartials.partialWithRespectTo(x) == approx(-0.25)

def testPartialAtUsingVariableName():
    x = Variable("x")
    z = x ** Constant(2)
    partial = z.partialAt(VariableValues({ "x": 3 }), "x")
    assert partial == approx(6)

def testEquality():
    c = Constant(7)
    assert c == c
    assert c == Constant(7)
    assert c == Constant(7.0)
    assert c != Constant(8)
    x = Variable("x")
    assert x == x
    assert x != Variable("y")
    assert x == Variable("x")
    assert x != c
    z = x ** c
    assert z == z
    assert z == x ** c
    assert z != c
    assert z != x
    assert z != x ** c + Constant(1)
