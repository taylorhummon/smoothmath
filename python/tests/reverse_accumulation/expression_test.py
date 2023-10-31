from pytest import approx, raises
import math
from src.reverse_accumulation.custom_exceptions import MathException
from src.reverse_accumulation.expression import *

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
    assert z.evaluate({ x: 2 }) == -2
    result = z.derive({ x: 2 })
    assert result.partialWithRespectTo(x) == -1

### Reciprocal

def testReciprocal():
    x = Variable()
    z = Reciprocal(x)
    assert z.evaluate({ x: 2 }) == approx(0.5)
    result = z.derive({ x: 2 })
    assert result.partialWithRespectTo(x) == approx(-0.25)
    with raises(MathException):
        z.evaluate({ x: 0 })
    with raises(MathException):
        z.derive({ x: 0 })
    assert z.evaluate({ x: -1 }) == approx(-1.0)
    result = z.derive({ x: -1 })
    assert result.partialWithRespectTo(x) == approx(-1.0)

### Square Root

def testSquareRoot():
    x = Variable()
    z = SquareRoot(x)
    assert z.evaluate({ x: 4 }) == approx(2.0)
    result = z.derive({ x: 4 })
    assert result.partialWithRespectTo(x) == approx(0.25)
    with raises(MathException):
        z.evaluate({ x: 0 })
    with raises(MathException):
        z.derive({ x: 0 })
    with raises(MathException):
        z.evaluate({ x: -1 })
    with raises(MathException):
        z.derive({ x: -1 })

### Natural Exponential

def testNaturalExponential():
    x = Variable()
    z = NaturalExponential(x)
    assert z.evaluate({ x: 0 }) == approx(1.0)
    result = z.derive({ x: 0 })
    assert result.partialWithRespectTo(x) == approx(1.0)
    assert z.evaluate({ x: 1 }) == approx(math.e)
    result = z.derive({ x: 1 })
    assert result.partialWithRespectTo(x) == approx(math.e)
    assert z.evaluate({ x: -1 }) == approx(1.0 / math.e)
    result = z.derive({ x: -1 })
    assert result.partialWithRespectTo(x) == approx(1.0 / math.e)

### Natural Logarithm

def testNaturalLogarithm():
    x = Variable()
    z = NaturalLogarithm(x)
    assert z.evaluate({ x: 1 }) == approx(0.0)
    result = z.derive({ x: 1 })
    assert result.partialWithRespectTo(x) == approx(1.0)
    result = z.derive({ x: math.e })
    assert result.partialWithRespectTo(x) == approx(1.0 / math.e)
    assert z.evaluate({ x: math.e }) == approx(1.0)
    with raises(MathException):
        z.evaluate({ x: 0.0 })
    with raises(MathException):
        z.derive({ x: 0.0 })
    with raises(MathException):
        z.evaluate({ x: -1.0 })
    with raises(MathException):
        z.derive({ x: -1.0 })

### Sine

def testSine():
    theta = Variable()
    z = Sine(theta)
    assert z.evaluate({ theta: 0.0 }) == approx(0.0)
    result = z.derive({ theta: 0.0 })
    assert result.partialWithRespectTo(theta) == approx(1.0)
    assert z.evaluate({ theta: math.pi / 2 }) == approx(1.0)
    result = z.derive({ theta: math.pi / 2 })
    assert result.partialWithRespectTo(theta) == approx(0.0)

### Cosine

def testCosine():
    theta = Variable()
    z = Cosine(theta)
    assert z.evaluate({ theta: 0.0 }) == approx(1.0)
    result = z.derive({ theta: 0.0 })
    assert result.partialWithRespectTo(theta) == approx(0.0)
    assert z.evaluate({ theta: math.pi / 2 }) == approx(0.0)
    result = z.derive({ theta: math.pi / 2 })
    assert result.partialWithRespectTo(theta) == approx(-1.0)

### Plus

def testPlus():
    x = Variable()
    y = Variable()
    z = Plus(x, y)
    assert z.evaluate({ x: 2, y: 3 }) == approx(5.0)
    result = z.derive({ x: 2, y: 3 })
    assert result.partialWithRespectTo(x) == approx(1.0)
    assert result.partialWithRespectTo(y) == approx(1.0)

### Minus

def testMinus():
    x = Variable()
    y = Variable()
    z = Minus(x, y)
    assert z.evaluate({ x: 2, y: 3 }) == approx(-1.0)
    result = z.derive({ x: 2, y: 3 })
    assert result.partialWithRespectTo(x) == approx(1.0)
    assert result.partialWithRespectTo(y) == approx(-1.0)

### Multiply

def testMultiply():
    x = Variable()
    y = Variable()
    z = Multiply(x, y)
    assert z.evaluate({ x: 2, y: 3 }) == approx(6.0)
    result = z.derive({ x: 2, y: 3 })
    assert result.partialWithRespectTo(x) == approx(3.0)
    assert result.partialWithRespectTo(y) == approx(2.0)

### Divide

def testDivide():
    x = Variable()
    y = Variable()
    z = Divide(x, y)
    assert z.evaluate({ x: 5, y: 2 }) == approx(2.5)
    result = z.derive({ x: 5, y: 2 })
    assert result.partialWithRespectTo(x) == approx(0.5)
    assert result.partialWithRespectTo(y) == approx(-1.25)
    with raises(MathException):
        z.evaluate({ x: 3.0, y: 0.0 })
    with raises(MathException):
        z.derive({ x: 3.0, y: 0.0 })

### PowerWithIntegralExponent

def testPowerWithIntegralExponent():
    x = Variable()
    c = Constant(2)
    z = Power(x, c)
    assert z.evaluate({ x: 3 }) == approx(9.0)
    result = z.derive({ x: 3 })
    assert result.partialWithRespectTo(x) == approx(6.0)
    assert z.evaluate({ x: 0 }) == approx(0.0)
    result = z.derive({ x: 0 })
    assert result.partialWithRespectTo(x) == approx(0.0)
    assert z.evaluate({ x: -5 }) == approx(25.0)
    result = z.derive({ x: -5 })
    assert result.partialWithRespectTo(x) == approx(-10.0)

def testPowerWithNegativeIntegralExponent():
    x = Variable()
    c = Constant(-2)
    z = Power(x, c)
    assert z.evaluate({ x: 2 }) == approx(0.25)
    result = z.derive({ x: 2 })
    assert result.partialWithRespectTo(x) == approx(-0.25)
    with raises(MathException):
        z.evaluate({ x: 0 })
    with raises(MathException):
        z.derive({ x: 0 })
    assert z.evaluate({ x: -2 }) == approx(0.25)
    result = z.derive({ x: -2 })
    assert result.partialWithRespectTo(x) == approx(0.25)

def testIllFormedPowerWithIntegralExponent():
    x = Variable()
    c = Constant(3.5) # we're only supposed to put integers in the exponent
    z = Power(x, c)
    with raises(Exception):
        z.evaluate({ x: -2 })
    with raises(Exception):
        z.evaluate({ x: -2 })

### Power

def testPower():
    x = Variable()
    y = Variable()
    z = Power(x, y)
    assert z.evaluate({ x: 3.0, y: 2.5 }) == approx(15.588457268)
    result = z.derive({ x: 3.0, y: 2.5 })
    assert result.partialWithRespectTo(x) == approx(12.990381056)
    assert result.partialWithRespectTo(y) == approx(17.125670716)
    with raises(MathException):
        z.evaluate({ x: 0.0, y: 2.5 })
    with raises(MathException):
        z.derive({ x: 0.0, y: 2.5 })
    with raises(MathException):
        z.evaluate({ x: -3.0, y: 2.5 })
    with raises(MathException):
        z.derive({ x: -3.0, y: 2.5 })
    assert z.evaluate({ x: 3.0, y: 0.0 }) == approx(1.0)
    result = z.derive({ x: 3.0, y: 0.0 })
    assert result.partialWithRespectTo(x) == approx(0.0)
    assert result.partialWithRespectTo(y) == approx(1.0986122886)
    assert z.evaluate({ x: 3.0, y: -2.5 }) == approx(0.0641500299)
    result = z.derive({ x: 3.0, y: -2.5 })
    assert result.partialWithRespectTo(x) == approx(-0.0534583582)
    assert result.partialWithRespectTo(y) == approx(0.0704760111)
    with raises(MathException):
        z.evaluate({ x: 0.0, y: 0.0 })
    with raises(MathException):
        z.derive({ x: 0.0, y: 0.0 })

### Polynomials

def testPolynomialOfOneVariable():
    x = Variable()
    z = x * x - Constant(6) * x + Constant(4)
    assert z.evaluate({ x: 2 }) == -4
    result = z.derive({ x: 2 })
    assert result.partialWithRespectTo(x) == -2

def testPolynomialOfTwoVariables():
    x = Variable()
    y = Variable()
    z = x * (x + y) - Constant(5) * y * y
    assert z.evaluate({ x: 2, y: 3 }) == -35
    result = z.derive({ x: 2, y: 3 })
    assert result.partialWithRespectTo(x) == 7
    assert result.partialWithRespectTo(y) == -28

def testPolynomialOfThreeVariables():
    w = Variable()
    x = Variable()
    y = Variable()
    z = w * w + Constant(5) * w * x * x - w * x * y
    assert z.evaluate({ w: 2, x: 3, y: 4 }) == 70
    result = z.derive({ w: 2, x: 3, y: 4 })
    assert result.partialWithRespectTo(w) == 37
    assert result.partialWithRespectTo(x) == 52
    assert result.partialWithRespectTo(y) == -6

### Other

def testCompositeFunctionEvaluation():
    x = Variable()
    z = NaturalExponential(x ** Constant(2))
    assert z.evaluate({ x: 2 }) == approx(54.598150033)

def testCompositeFunctionDerivation():
    x = Variable()
    z = NaturalExponential(x ** Constant(2))
    result = z.derive({ x: 2 })
    assert result.partialWithRespectTo(x) == approx(218.392600132)

def testExpressionReuseEvaluation():
    x = Variable()
    w = x ** Constant(2)
    z = (w + Constant(1)) / w
    assert z.evaluate({ x: 2 }) == approx(1.25)

def testExpressionReuseDerivation():
    x = Variable()
    w = x ** Constant(2)
    z = (w + Constant(1)) / w
    result = z.derive({ x: 2 })
    assert result.partialWithRespectTo(x) == approx(-0.25)
