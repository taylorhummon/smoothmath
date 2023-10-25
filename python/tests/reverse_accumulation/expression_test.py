from pytest import approx, raises
import math
from src.reverse_accumulation.expression import *

### Constant

def testConstant():
    c = Constant(7)
    assert c.value == 7
    computedPartials = c.derive()
    x = Variable(2)
    assert computedPartials.partialWithRespectTo(x) == 0

### Variable

def testVariable():
    x = Variable(2)
    assert x.value == 2
    computedPartials = x.derive()
    assert computedPartials.partialWithRespectTo(x) == 1
    y = Variable(3)
    assert computedPartials.partialWithRespectTo(y) == 0

### Negation

def testNegation():
    x = Variable(2)
    z = Negation(x)
    computedPartials = z.derive()
    assert z.value == -2
    assert computedPartials.partialWithRespectTo(x) == -1

# ### Reciprocal

def testReciprocal():
    x = Variable(2)
    z = Reciprocal(x)
    computedPartials = z.derive()
    assert z.value == approx(0.5)
    assert computedPartials.partialWithRespectTo(x) == approx(-0.25)

def testReciprocalAtZero():
    x = Variable(0)
    z = Reciprocal(x)
    with raises(Exception):
        z.derive()

### Natural Exponential

def testNaturalExponentialAtZero():
    x = Variable(0)
    z = NaturalExponential(x)
    computedPartials = z.derive()
    assert z.value == approx(1.0)
    assert computedPartials.partialWithRespectTo(x) == approx(1.0)

def testNaturalExponentialAtOne():
    x = Variable(1)
    z = NaturalExponential(x)
    computedPartials = z.derive()
    assert z.value == approx(math.e)
    assert computedPartials.partialWithRespectTo(x) == approx(math.e)

### Natural Logarithm

def testNaturalLogarithmAtOne():
    x = Variable(1)
    z = NaturalLogarithm(x)
    computedPartials = z.derive()
    assert z.value == approx(0.0)
    assert computedPartials.partialWithRespectTo(x) == approx(1.0)

def testNaturalLogarithmAtE():
    x = Variable(math.e)
    z = NaturalLogarithm(x)
    computedPartials = z.derive()
    assert z.value == approx(1.0)
    assert computedPartials.partialWithRespectTo(x) == approx(1.0 / math.e)

def testNaturalLogarithmAt0():
    x = Variable(0.0)
    z = NaturalLogarithm(x)
    with raises(Exception):
        z.derive()

def testNaturalLogarithmAtNegative():
    x = Variable(-3.0)
    z = NaturalLogarithm(x)
    with raises(Exception):
        z.derive()

### Sine

def testSineAt0():
    theta = Variable(0.0)
    z = Sine(theta)
    computedPartials = z.derive()
    assert z.value == approx(0.0)
    assert computedPartials.partialWithRespectTo(theta) == approx(1.0)

def testSineAtOneQuarterTurn():
    theta = Variable(math.pi / 2)
    z = Sine(theta)
    computedPartials = z.derive()
    assert z.value == approx(1.0)
    assert computedPartials.partialWithRespectTo(theta) == approx(0.0)

### Cosine

def testCosineAt0():
    theta = Variable(0.0)
    z = Cosine(theta)
    computedPartials = z.derive()
    assert z.value == approx(1.0)
    assert computedPartials.partialWithRespectTo(theta) == approx(0.0)

def testCosineAtOneQuarterTurn():
    theta = Variable(math.pi / 2)
    z = Cosine(theta)
    computedPartials = z.derive()
    assert z.value == approx(0.0)
    assert computedPartials.partialWithRespectTo(theta) == approx(-1.0)

### Plus

def testPlus():
    x = Variable(2)
    y = Variable(3)
    z = Plus(x, y)
    computedPartials = z.derive()
    assert z.value == approx(5.0)
    assert computedPartials.partialWithRespectTo(x) == approx(1.0)
    assert computedPartials.partialWithRespectTo(y) == approx(1.0)

### Minus

def testMinus():
    x = Variable(2)
    y = Variable(3)
    z = Minus(x, y)
    computedPartials = z.derive()
    assert z.value == approx(-1.0)
    assert computedPartials.partialWithRespectTo(x) == approx(1.0)
    assert computedPartials.partialWithRespectTo(y) == approx(-1.0)

### Multiply

def testMultiply():
    x = Variable(2)
    y = Variable(3)
    z = Multiply(x, y)
    computedPartials = z.derive()
    assert z.value == approx(6.0)
    assert computedPartials.partialWithRespectTo(x) == approx(3.0)
    assert computedPartials.partialWithRespectTo(y) == approx(2.0)

### Divide

def testDivide():
    x = Variable(5)
    y = Variable(2)
    z = Divide(x, y)
    computedPartials = z.derive()
    assert z.value == approx(2.5)
    assert computedPartials.partialWithRespectTo(x) == approx(0.5)
    assert computedPartials.partialWithRespectTo(y) == approx(-1.25)

### PowerWithIntegralExponent

def testPowerWithIntegralExponent():
    x = Variable(3)
    c = Constant(2)
    z = PowerWithIntegralExponent(x, c)
    computedPartials = z.derive()
    assert z.value == approx(9.0)
    assert computedPartials.partialWithRespectTo(x) == approx(6.0)

def testPowerWithIntegralExponentAndNegativeBase():
    x = Variable(-5)
    c = Constant(2)
    z = PowerWithIntegralExponent(x, c)
    computedPartials = z.derive()
    assert z.value == approx(25.0)
    assert computedPartials.partialWithRespectTo(x) == approx(-10.0)

def testPowerWithIntegralExponentAndZeroBase():
    x = Variable(0)
    c = Constant(2)
    z = PowerWithIntegralExponent(x, c)
    computedPartials = z.derive()
    assert z.value == approx(0.0)
    assert computedPartials.partialWithRespectTo(x) == approx(0.0)

def testPowerWithNegativeIntegralExponent():
    x = Variable(2)
    c = Constant(-2)
    z = PowerWithIntegralExponent(x, c)
    computedPartials = z.derive()
    assert z.value == approx(0.25)
    assert computedPartials.partialWithRespectTo(x) == approx(-0.25)

def testPowerWithNegativeIntegralExponentAndNegativeBase():
    x = Variable(-2)
    c = Constant(-2)
    z = PowerWithIntegralExponent(x, c)
    computedPartials = z.derive()
    assert z.value == approx(0.25)
    assert computedPartials.partialWithRespectTo(x) == approx(0.25)

def testPowerWithNegativeIntegralExponentAndZeroBase():
    x = Variable(0)
    c = Constant(-2)
    z = PowerWithIntegralExponent(x, c)
    with raises(Exception):
        z.derive()

### Power

def testPower():
    x = Variable(3.0)
    y = Variable(2.5)
    z = Power(x, y)
    computedPartials = z.derive()
    assert z.value == approx(15.588457268)
    assert computedPartials.partialWithRespectTo(x) == approx(12.990381056)
    assert computedPartials.partialWithRespectTo(y) == approx(17.125670716)

def testPowerWithNegativeBase():
    x = Variable(-3.0)
    y = Variable(2.5)
    z = Power(x, y)
    with raises(Exception):
        z.derive()

def testPowerWithZeroBase():
    x = Variable(0.0)
    y = Variable(2.5)
    z = Power(x, y)
    with raises(Exception):
        z.derive()

def testPowerWithNegativeExponent():
    x = Variable(3.0)
    y = Variable(-2.5)
    z = Power(x, y)
    computedPartials = z.derive()
    assert z.value == approx(0.0641500299)
    assert computedPartials.partialWithRespectTo(x) == approx(-0.0534583582)
    assert computedPartials.partialWithRespectTo(y) == approx(0.0704760111)

def testPowerWithZeroExponent():
    x = Variable(3.0)
    y = Variable(0.0)
    z = Power(x, y)
    computedPartials = z.derive()
    assert z.value == approx(1.0)
    assert computedPartials.partialWithRespectTo(x) == approx(0.0)
    assert computedPartials.partialWithRespectTo(y) == approx(1.0986122886)

def testPowerWithZeroBaseAndZeroExponent():
    x = Variable(0.0)
    y = Variable(0.0)
    z = Power(x, y)
    with raises(Exception):
        z.derive()

### Polynomials

def testPolynomialOfOneVariable():
    x = Variable(2)
    z = x * x - Constant(6) * x + Constant(4)
    computedPartials = z.derive()
    assert z.value == -4
    assert computedPartials.partialWithRespectTo(x) == -2

def testPolynomialOfTwoVariables():
    x = Variable(2)
    y = Variable(3)
    z = x * (x + y) - Constant(5) * y * y
    computedPartials = z.derive()
    assert z.value == -35
    assert computedPartials.partialWithRespectTo(x) == 7
    assert computedPartials.partialWithRespectTo(y) == -28

def testPolynomialOfThreeVariables():
    w = Variable(2)
    x = Variable(3)
    y = Variable(4)
    z = w * w + Constant(5) * w * x * x - w * x * y
    computedPartials = z.derive()
    assert z.value == 70
    assert computedPartials.partialWithRespectTo(w) == 37
    assert computedPartials.partialWithRespectTo(x) == 52
    assert computedPartials.partialWithRespectTo(y) == -6

### Other

def testCompositeFunction():
    x = Variable(2)
    z = NaturalExponential(x ** Constant(2))
    computedPartials = z.derive()
    assert z.value == approx(54.598150033)
    assert computedPartials.partialWithRespectTo(x) == approx(218.392600132)

def testExpressionReuse():
    x = Variable(2)
    w = x ** Constant(2)
    z = (w + Constant(1)) / w
    computedPartials = z.derive()
    assert z.value == approx(1.25)
    assert computedPartials.partialWithRespectTo(x) == approx(-0.25)
