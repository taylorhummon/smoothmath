from pytest import approx, raises
from src.smooth_expression.custom_exceptions import DomainException
from src.smooth_expression.constant import Constant
from src.smooth_expression.variable import Variable
from src.smooth_expression.exponential import Exponential

def testPolynomialOfOneVariable():
    x = Variable("x")
    z = x * x - Constant(6) * x + Constant(4)
    partial = z.deriveSingle({ x: 2 }, x)
    assert partial == -2

def testPolynomialOfTwoVariables():
    x = Variable("x")
    y = Variable("y")
    z = x * (x + y) - Constant(5) * y * y
    variableValues = { x: 2, y: 3 }
    partialWithRespectToX = z.deriveSingle(variableValues, x)
    assert partialWithRespectToX == 7
    partialWithRespectToY = z.deriveSingle(variableValues, y)
    assert partialWithRespectToY == -28

def testPolynomialOfThreeVariables():
    w = Variable("w")
    x = Variable("x")
    y = Variable("y")
    z = w * w + Constant(5) * w * x * x - w * x * y
    variableValues = { w: 2, x: 3, y: 4 }
    partialWithRespectToW = z.deriveSingle(variableValues, w)
    assert partialWithRespectToW == 37
    partialWithRespectToX = z.deriveSingle(variableValues, x)
    assert partialWithRespectToX == 52
    partialWithRespectToY = z.deriveSingle(variableValues, y)
    assert partialWithRespectToY == -6

def testUnrelatedVariable():
    x = Variable("x")
    y = Variable("y")
    z = x ** Constant(2)
    partial = z.deriveSingle({ x: 2 }, y)
    assert partial == 0

def testCompositeFunction():
    x = Variable("x")
    z = Exponential(x ** Constant(2))
    partial = z.deriveSingle({ x: 2 }, x)
    assert partial == approx(218.392600132)

def testIndeterminateForm():
    t = Variable("t")
    z = (Constant(2) * t) / t
    with raises(DomainException):
        z.deriveSingle({ t: 0 }, t)

def testExpressionReuse():
    x = Variable("x")
    w = x ** Constant(2)
    z = (w + Constant(1)) / w
    partial = z.deriveSingle({ x: 2 }, x)
    assert partial == approx(-0.25)

def testPolynomialOfOneVariableMulti():
    x = Variable("x")
    z = x * x - Constant(6) * x + Constant(4)
    multiResult = z.deriveMulti({ x: 2 })
    assert multiResult.value == -4
    assert multiResult.partialWithRespectTo(x) == -2

def testPolynomialOfTwoVariablesMulti():
    x = Variable("x")
    y = Variable("y")
    z = x * (x + y) - Constant(5) * y * y
    multiResult = z.deriveMulti({ x: 2, y: 3 })
    assert multiResult.value == -35
    assert multiResult.partialWithRespectTo(x) == 7
    assert multiResult.partialWithRespectTo(y) == -28

def testPolynomialOfThreeVariablesMulti():
    w = Variable("w")
    x = Variable("x")
    y = Variable("y")
    z = w * w + Constant(5) * w * x * x - w * x * y
    multiResult = z.deriveMulti({ w: 2, x: 3, y: 4 })
    assert multiResult.value == 70
    assert multiResult.partialWithRespectTo(w) == 37
    assert multiResult.partialWithRespectTo(x) == 52
    assert multiResult.partialWithRespectTo(y) == -6

def testUnrelatedVariableMulti():
    x = Variable("x")
    y = Variable("y")
    z = x ** Constant(2)
    multiResult = z.deriveMulti({ x: 2 })
    assert multiResult.value == 4
    assert multiResult.partialWithRespectTo(y) == 0

def testCompositeFunctionMulti():
    x = Variable("x")
    z = Exponential(x ** Constant(2))
    multiResult = z.deriveMulti({ x: 2 })
    assert multiResult.value == approx(54.598150033)
    assert multiResult.partialWithRespectTo(x) == approx(218.392600132)

def testIndeterminateFormMulti():
    t = Variable("t")
    z = (Constant(2) * t) / t
    with raises(DomainException):
        z.deriveMulti({ t: 0 })

def testExpressionReuseMulti():
    x = Variable("x")
    w = x ** Constant(2)
    z = (w + Constant(1)) / w
    multiResult = z.deriveMulti({ x: 2 })
    assert multiResult.value == approx(1.25)
    assert multiResult.partialWithRespectTo(x) == approx(-0.25)
