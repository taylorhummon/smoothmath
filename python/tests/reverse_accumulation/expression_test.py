from pytest import approx, raises
import math
from src.reverse_accumulation.custom_exceptions import DomainException
from src.reverse_accumulation.expression import (
    Constant, Variable,
    Negation, Reciprocal, SquareRoot, NaturalExponential, NaturalLogarithm, Sine, Cosine,
    Plus, Minus, Multiply, Divide, Power,
)

### Constant

def testConstant():
    c = Constant(7)
    assert c.evaluate({}) == 7
    x = Variable()
    result = c.derive({ x: 2 })
    assert result.partialWithRespectTo(x) == 0

### Variable

def testVariable():
    x = Variable()
    assert x.evaluate({ x: 2 }) == 2
    y = Variable()
    result = x.derive({ x: 2, y: 3 })
    assert result.partialWithRespectTo(x) == 1
    assert result.partialWithRespectTo(y) == 0

### Negation

def testNegation():
    x = Variable()
    z = Negation(x)
    variableValues = { x: 2 }
    assert z.evaluate(variableValues) == -2
    result = z.derive(variableValues)
    assert result.partialWithRespectTo(x) == -1

### Reciprocal

def testReciprocal():
    x = Variable()
    z = Reciprocal(x)
    variableValues = { x: 2 }
    assert z.evaluate(variableValues) == approx(0.5)
    result = z.derive(variableValues)
    assert result.partialWithRespectTo(x) == approx(-0.25)
    variableValues = { x: 0 }
    with raises(DomainException):
        z.evaluate(variableValues)
    with raises(DomainException):
        z.derive(variableValues)
    variableValues = { x: -1 }
    assert z.evaluate(variableValues) == approx(-1.0)
    result = z.derive(variableValues)
    assert result.partialWithRespectTo(x) == approx(-1.0)

### Square Root

def testSquareRoot():
    x = Variable()
    z = SquareRoot(x)
    variableValues = { x: 4 }
    assert z.evaluate(variableValues) == approx(2.0)
    result = z.derive(variableValues)
    assert result.partialWithRespectTo(x) == approx(0.25)
    variableValues = { x: 0 }
    with raises(DomainException):
        z.evaluate(variableValues)
    with raises(DomainException):
        z.derive(variableValues)
    variableValues = { x: -1 }
    with raises(DomainException):
        z.evaluate(variableValues)
    with raises(DomainException):
        z.derive(variableValues)

### Natural Exponential

def testNaturalExponential():
    x = Variable()
    z = NaturalExponential(x)
    variableValues = { x: 0 }
    assert z.evaluate(variableValues) == approx(1.0)
    result = z.derive(variableValues)
    assert result.partialWithRespectTo(x) == approx(1.0)
    variableValues = { x: 1 }
    assert z.evaluate(variableValues) == approx(math.e)
    result = z.derive(variableValues)
    assert result.partialWithRespectTo(x) == approx(math.e)
    variableValues = { x: -1 }
    assert z.evaluate(variableValues) == approx(1.0 / math.e)
    result = z.derive(variableValues)
    assert result.partialWithRespectTo(x) == approx(1.0 / math.e)

### Natural Logarithm

def testNaturalLogarithm():
    x = Variable()
    z = NaturalLogarithm(x)
    variableValues = { x: 1 }
    assert z.evaluate(variableValues) == approx(0.0)
    result = z.derive(variableValues)
    assert result.partialWithRespectTo(x) == approx(1.0)
    variableValues = { x: math.e }
    result = z.derive(variableValues)
    assert result.partialWithRespectTo(x) == approx(1.0 / math.e)
    assert z.evaluate(variableValues) == approx(1.0)
    variableValues = { x: 0.0 }
    with raises(DomainException):
        z.evaluate(variableValues)
    with raises(DomainException):
        z.derive(variableValues)
    variableValues = { x: -1.0 }
    with raises(DomainException):
        z.evaluate(variableValues)
    with raises(DomainException):
        z.derive(variableValues)

### Sine

def testSine():
    theta = Variable()
    z = Sine(theta)
    variableValues = { theta: 0.0 }
    assert z.evaluate(variableValues) == approx(0.0)
    result = z.derive(variableValues)
    assert result.partialWithRespectTo(theta) == approx(1.0)
    variableValues = { theta: math.pi / 2 } # one quarter turn
    assert z.evaluate(variableValues) == approx(1.0)
    result = z.derive(variableValues)
    assert result.partialWithRespectTo(theta) == approx(0.0)

### Cosine

def testCosine():
    theta = Variable()
    z = Cosine(theta)
    variableValues = { theta: 0.0 }
    assert z.evaluate(variableValues) == approx(1.0)
    result = z.derive(variableValues)
    assert result.partialWithRespectTo(theta) == approx(0.0)
    variableValues = { theta: math.pi / 2 } # one quarter turn
    assert z.evaluate(variableValues) == approx(0.0)
    result = z.derive(variableValues)
    assert result.partialWithRespectTo(theta) == approx(-1.0)

### Plus

def testPlus():
    x = Variable()
    y = Variable()
    z = Plus(x, y)
    variableValues = { x: 2, y: 3 }
    assert z.evaluate(variableValues) == approx(5.0)
    result = z.derive(variableValues)
    assert result.partialWithRespectTo(x) == approx(1.0)
    assert result.partialWithRespectTo(y) == approx(1.0)

### Minus

def testMinus():
    x = Variable()
    y = Variable()
    z = Minus(x, y)
    variableValues = { x: 2, y: 3 }
    assert z.evaluate(variableValues) == approx(-1.0)
    result = z.derive(variableValues)
    assert result.partialWithRespectTo(x) == approx(1.0)
    assert result.partialWithRespectTo(y) == approx(-1.0)

### Multiply

def testMultiply():
    x = Variable()
    y = Variable()
    z = Multiply(x, y)
    variableValues = { x: 2, y: 3 }
    assert z.evaluate(variableValues) == approx(6.0)
    result = z.derive(variableValues)
    assert result.partialWithRespectTo(x) == approx(3.0)
    assert result.partialWithRespectTo(y) == approx(2.0)

### Divide

def testDivide():
    x = Variable()
    y = Variable()
    z = Divide(x, y)
    variableValues = { x: 5, y: 2 }
    assert z.evaluate(variableValues) == approx(2.5)
    result = z.derive(variableValues)
    assert result.partialWithRespectTo(x) == approx(0.5)
    assert result.partialWithRespectTo(y) == approx(-1.25)
    variableValues = { x: 3.0, y: 0.0 }
    with raises(DomainException):
        z.evaluate(variableValues)
    with raises(DomainException):
        z.derive(variableValues)
    variableValues = { x: 0.0, y: 0.0 }
    with raises(DomainException):
        z.evaluate(variableValues)
    with raises(DomainException):
        z.derive(variableValues)

def testDivideWithConstantNumeratorZero():
    y = Variable()
    z = Divide(Constant(0), y)
    variableValues = { y: 3.0 }
    assert z.evaluate(variableValues) == approx(0.0)
    result = z.derive(variableValues)
    assert result.partialWithRespectTo(y) == approx(0.0)
    variableValues = { y: 0.0 }
    assert z.evaluate(variableValues) == approx(0.0)
    result = z.derive(variableValues)
    assert result.partialWithRespectTo(y) == approx(0.0)

def testDivideWithConstantDenominatorOne():
    x = Variable()
    z = Divide(x, Constant(1))
    variableValues = { x: 3.0 }
    assert z.evaluate(variableValues) == approx(3.0)
    result = z.derive(variableValues)
    assert result.partialWithRespectTo(x) == approx(1.0)
    variableValues = { x: 0.0 }
    assert z.evaluate(variableValues) == approx(0.0)
    result = z.derive(variableValues)
    assert result.partialWithRespectTo(x) == approx(1.0)

def testDivideWithConstantDenominatorZero():
    x = Variable()
    z = Divide(x, Constant(0))
    variableValues = { x: 3.0 }
    with raises(DomainException):
        z.evaluate(variableValues)
    with raises(DomainException):
        z.derive(variableValues)
    variableValues = { x: 0.0 }
    with raises(DomainException):
        z.evaluate(variableValues)
    with raises(DomainException):
        z.derive(variableValues)

### Power

def testPower():
    x = Variable()
    y = Variable()
    z = Power(x, y)
    variableValues = { x: 3.0, y: 2.5 }
    assert z.evaluate(variableValues) == approx(15.588457268)
    result = z.derive(variableValues)
    assert result.partialWithRespectTo(x) == approx(12.990381056)
    assert result.partialWithRespectTo(y) == approx(17.125670716)
    variableValues = { x: 3.0, y: 0.0 }
    assert z.evaluate(variableValues) == approx(1.0)
    result = z.derive(variableValues)
    assert result.partialWithRespectTo(x) == approx(0.0)
    assert result.partialWithRespectTo(y) == approx(1.0986122886)
    variableValues = { x: 3.0, y: -2.5 }
    assert z.evaluate(variableValues) == approx(0.0641500299)
    result = z.derive(variableValues)
    assert result.partialWithRespectTo(x) == approx(-0.0534583582)
    assert result.partialWithRespectTo(y) == approx(0.0704760111)
    variableValues = { x: 0.0, y: 2.5 }
    with raises(DomainException):
        z.evaluate(variableValues)
    with raises(DomainException):
        z.derive(variableValues)
    variableValues = { x: 0.0, y: 0.0 }
    with raises(DomainException):
        z.evaluate(variableValues)
    with raises(DomainException):
        z.derive(variableValues)
    variableValues = { x: 0.0, y: -2.5 }
    with raises(DomainException):
        z.evaluate(variableValues)
    with raises(DomainException):
        z.derive(variableValues)
    variableValues = { x: -3.0, y: 2.5 }
    with raises(DomainException):
        z.evaluate(variableValues)
    with raises(DomainException):
        z.derive(variableValues)
    variableValues = { x: -3.0, y: 0.0 }
    with raises(DomainException):
        z.evaluate(variableValues)
    with raises(DomainException):
        z.derive(variableValues)
    variableValues = { x: -3.0, y: -2.5 }
    with raises(DomainException):
        z.evaluate(variableValues)
    with raises(DomainException):
        z.derive(variableValues)

def testPowerWithConstantBaseOne():
    y = Variable()
    z = Power(Constant(1), y)
    variableValues = { y: 3 }
    assert z.evaluate(variableValues) == approx(1.0)
    result = z.derive(variableValues)
    assert result.partialWithRespectTo(y) == approx(0.0)
    variableValues = { y: 0 }
    assert z.evaluate(variableValues) == approx(1.0)
    result = z.derive(variableValues)
    assert result.partialWithRespectTo(y) == approx(0.0)
    variableValues = { y: -5 }
    assert z.evaluate(variableValues) == approx(1.0)
    result = z.derive(variableValues)
    assert result.partialWithRespectTo(y) == approx(0.0)

def testPowerWithConstantBaseZero():
    y = Variable()
    z = Power(Constant(0), y)
    variableValues = { y: 3 }
    with raises(DomainException):
        z.evaluate(variableValues)
    with raises(DomainException):
        z.derive(variableValues)
    variableValues = { y: 0 }
    with raises(DomainException):
        z.evaluate(variableValues)
    with raises(DomainException):
        z.derive(variableValues)
    variableValues = { y: -5 }
    with raises(DomainException):
        z.evaluate(variableValues)
    with raises(DomainException):
        z.derive(variableValues)

def testPowerWithConstantBaseNegativeOne():
    y = Variable()
    z = Power(Constant(-1), y)
    variableValues = { y: 3 }
    with raises(DomainException):
        z.evaluate(variableValues)
    with raises(DomainException):
        z.derive(variableValues)
    variableValues = { y: 0 }
    with raises(DomainException):
        z.evaluate(variableValues)
    with raises(DomainException):
        z.derive(variableValues)
    variableValues = { y: -5 }
    with raises(DomainException):
        z.evaluate(variableValues)
    with raises(DomainException):
        z.derive(variableValues)

def testPowerWithConstantExponentTwo():
    x = Variable()
    z = Power(x, Constant(2))
    variableValues = { x: 3 }
    assert z.evaluate(variableValues) == approx(9.0)
    result = z.derive(variableValues)
    assert result.partialWithRespectTo(x) == approx(6.0)
    variableValues = { x: 0 }
    assert z.evaluate(variableValues) == approx(0.0)
    result = z.derive(variableValues)
    assert result.partialWithRespectTo(x) == approx(0.0)
    variableValues = { x: -5 }
    assert z.evaluate(variableValues) == approx(25.0)
    result = z.derive(variableValues)
    assert result.partialWithRespectTo(x) == approx(-10.0)

def testPowerWithConstantExponentOne():
    x = Variable()
    z = Power(x, Constant(1))
    variableValues = { x: 3 }
    assert z.evaluate(variableValues) == approx(3.0)
    result = z.derive(variableValues)
    assert result.partialWithRespectTo(x) == approx(1.0)
    variableValues = { x: 0 }
    assert z.evaluate(variableValues) == approx(0.0)
    result = z.derive(variableValues)
    assert result.partialWithRespectTo(x) == approx(1.0)
    variableValues = { x: -5 }
    assert z.evaluate(variableValues) == approx(-5.0)
    result = z.derive(variableValues)
    assert result.partialWithRespectTo(x) == approx(1.0)

def testPowerWithConstantExponentZero():
    x = Variable()
    z = Power(x, Constant(0))
    variableValues = { x: 3 }
    assert z.evaluate(variableValues) == approx(1.0)
    result = z.derive(variableValues)
    assert result.partialWithRespectTo(x) == approx(0.0)
    variableValues = { x: 0 }
    assert z.evaluate(variableValues) == approx(1.0)
    result = z.derive(variableValues)
    assert result.partialWithRespectTo(x) == approx(0.0)
    variableValues = { x: -5 }
    assert z.evaluate(variableValues) == approx(1.0)
    result = z.derive(variableValues)
    assert result.partialWithRespectTo(x) == approx(0.0)

def testPowerWithConstantExponentNegativeOne():
    x = Variable()
    z = Power(x, Constant(-1))
    variableValues = { x: 2 }
    assert z.evaluate(variableValues) == approx(0.5)
    result = z.derive(variableValues)
    assert result.partialWithRespectTo(x) == approx(-0.25)
    variableValues = { x: 0 }
    with raises(DomainException):
        z.evaluate(variableValues)
    with raises(DomainException):
        z.derive(variableValues)
    variableValues = { x: -5 }
    assert z.evaluate(variableValues) == approx(-0.2)
    result = z.derive(variableValues)
    assert result.partialWithRespectTo(x) == approx(-0.04)

def testPowerWithConstantExponentNegativeTwo():
    x = Variable()
    z = Power(x, Constant(-2))
    variableValues = { x: 2 }
    assert z.evaluate(variableValues) == approx(0.25)
    result = z.derive(variableValues)
    assert result.partialWithRespectTo(x) == approx(-0.25)
    variableValues = { x: 0 }
    with raises(DomainException):
        z.evaluate(variableValues)
    with raises(DomainException):
        z.derive(variableValues)
    variableValues = { x: -5 }
    assert z.evaluate(variableValues) == approx(0.04)
    result = z.derive(variableValues)
    assert result.partialWithRespectTo(x) == approx(0.016)

def testPowerWithExponentMadeFromAddingConstants():
    x = Variable()
    z = Power(x, Constant(1) + Constant(1))
    variableValues = { x: 3 }
    assert z.evaluate(variableValues) == approx(9.0)
    result = z.derive(variableValues)
    assert result.partialWithRespectTo(x) == approx(6.0)
    variableValues = { x: 0 }
    assert z.evaluate(variableValues) == approx(0.0)
    result = z.derive(variableValues)
    assert result.partialWithRespectTo(x) == approx(0.0)
    variableValues = { x: -5 }
    assert z.evaluate(variableValues) == approx(25.0)
    result = z.derive(variableValues)
    assert result.partialWithRespectTo(x) == approx(-10.0)

### Polynomials

def testPolynomialOfOneVariable():
    x = Variable()
    z = x * x - Constant(6) * x + Constant(4)
    variableValues = { x: 2 }
    assert z.evaluate(variableValues) == -4
    result = z.derive(variableValues)
    assert result.partialWithRespectTo(x) == -2

def testPolynomialOfTwoVariables():
    x = Variable()
    y = Variable()
    z = x * (x + y) - Constant(5) * y * y
    variableValues = { x: 2, y: 3 }
    assert z.evaluate(variableValues) == -35
    result = z.derive(variableValues)
    assert result.partialWithRespectTo(x) == 7
    assert result.partialWithRespectTo(y) == -28

def testPolynomialOfThreeVariables():
    w = Variable()
    x = Variable()
    y = Variable()
    z = w * w + Constant(5) * w * x * x - w * x * y
    variableValues = { w: 2, x: 3, y: 4 }
    assert z.evaluate(variableValues) == 70
    result = z.derive(variableValues)
    assert result.partialWithRespectTo(w) == 37
    assert result.partialWithRespectTo(x) == 52
    assert result.partialWithRespectTo(y) == -6

### Other

def testCompositeFunction():
    x = Variable()
    z = NaturalExponential(x ** Constant(2))
    variableValues = { x: 2 }
    assert z.evaluate(variableValues) == approx(54.598150033)
    result = z.derive(variableValues)
    assert result.partialWithRespectTo(x) == approx(218.392600132)

def testIndeterminateForm():
    t = Variable()
    z = (Constant(2) * t) / t
    with raises(DomainException):
        z.derive({ t: 0 })

def testExpressionReuse():
    x = Variable()
    w = x ** Constant(2)
    z = (w + Constant(1)) / w
    variableValues = { x: 2 }
    assert z.evaluate(variableValues) == approx(1.25)
    result = z.derive(variableValues)
    assert result.partialWithRespectTo(x) == approx(-0.25)
