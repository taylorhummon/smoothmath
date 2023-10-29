from pytest import approx, raises
import math
from src.forward_accumulation.custom_exceptions import ArithmeticException
from src.forward_accumulation.expression import *

### Constant

def testConstant():
    c = Constant(7)
    assert c.value == 7
    x = Variable(2)
    result = c.derive(x)
    assert result.value == 7
    assert result.partial == 0

### Variable

def testVariable():
    x = Variable(2)
    result = x.derive(x)
    assert result.value == 2
    assert result.partial == 1

def testUnrelatedVariables():
    x = Variable(2)
    y = Variable(3)
    result = y.derive(x)
    assert result.value == 3
    assert result.partial == 0

### Negation

def testNegation():
    x = Variable(2)
    z = Negation(x)
    result = z.derive(x)
    assert result.value == -2
    assert result.partial == -1

### Reciprocal

def testReciprocal():
    x = Variable(2)
    z = Reciprocal(x)
    result = z.derive(x)
    assert result.value == approx(0.5)
    assert result.partial == approx(-0.25)

def testReciprocalAtZero():
    x = Variable(0)
    z = Reciprocal(x)
    with raises(ArithmeticException):
        z.derive(x)

### Natural Exponential

def testNaturalExponentialAtZero():
    x = Variable(0)
    z = NaturalExponential(x)
    result = z.derive(x)
    assert result.value == approx(1.0)
    assert result.partial == approx(1.0)

def testNaturalExponentialAtOne():
    x = Variable(1)
    z = NaturalExponential(x)
    result = z.derive(x)
    assert result.value == approx(math.e)
    assert result.partial == approx(math.e)

### Natural Logarithm

def testNaturalLogarithmAtOne():
    x = Variable(1)
    z = NaturalLogarithm(x)
    result = z.derive(x)
    assert result.value == approx(0.0)
    assert result.partial == approx(1.0)

def testNaturalLogarithmAtE():
    x = Variable(math.e)
    z = NaturalLogarithm(x)
    result = z.derive(x)
    assert result.value == approx(1.0)
    assert result.partial == approx(1.0 / math.e)

def testNaturalLogarithmAtZero():
    x = Variable(0.0)
    z = NaturalLogarithm(x)
    with raises(ArithmeticException):
        z.derive(x)

def testNaturalLogarithmAtNegative():
    x = Variable(-3.0)
    z = NaturalLogarithm(x)
    with raises(ArithmeticException):
        z.derive(x)

### Sine

def testSineAtZero():
    theta = Variable(0.0)
    z = Sine(theta)
    result = z.derive(theta)
    assert result.value == approx(0.0)
    assert result.partial == approx(1.0)

def testSineAtOneQuarterTurn():
    theta = Variable(math.pi / 2)
    z = Sine(theta)
    result = z.derive(theta)
    assert result.value == approx(1.0)
    assert result.partial == approx(0.0)

### Cosine

def testCosineAtZero():
    theta = Variable(0.0)
    z = Cosine(theta)
    result = z.derive(theta)
    assert result.value == approx(1.0)
    assert result.partial == approx(0.0)

def testCosineAtOneQuarterTurn():
    theta = Variable(math.pi / 2)
    z = Cosine(theta)
    result = z.derive(theta)
    assert result.value == approx(0.0)
    assert result.partial == approx(-1.0)

### Plus

def testPlus():
    x = Variable(2)
    y = Variable(3)
    z = Plus(x, y)
    resultForX = z.derive(x)
    assert resultForX.value == approx(5.0)
    assert resultForX.partial == approx(1.0)
    resultForY = z.derive(y)
    assert resultForY.value == approx(5.0)
    assert resultForY.partial == approx(1.0)

### Minus

def testMinus():
    x = Variable(2)
    y = Variable(3)
    z = Minus(x, y)
    resultForX = z.derive(x)
    assert resultForX.value == approx(-1.0)
    assert resultForX.partial == approx(1.0)
    resultForY = z.derive(y)
    assert resultForY.value == approx(-1.0)
    assert resultForY.partial == approx(-1.0)

### Multiply

def testMultiply():
    x = Variable(2)
    y = Variable(3)
    z = Multiply(x, y)
    resultForX = z.derive(x)
    assert resultForX.value == approx(6.0)
    assert resultForX.partial == approx(3.0)
    resultForY = z.derive(y)
    assert resultForY.value == approx(6.0)
    assert resultForY.partial == approx(2.0)

### Divide

def testDivide():
    x = Variable(5)
    y = Variable(2)
    z = Divide(x, y)
    resultForX = z.derive(x)
    assert resultForX.value == approx(2.5)
    assert resultForX.partial == approx(0.5)
    resultForY = z.derive(y)
    assert resultForY.value == approx(2.5)
    assert resultForY.partial == approx(-1.25)

### PowerWithIntegralExponent

def testPowerWithIntegralExponent():
    x = Variable(3)
    c = Constant(2)
    z = Power(x, c)
    result = z.derive(x)
    assert result.value == approx(9.0)
    assert result.partial == approx(6.0)

def testPowerWithIntegralExponentAndNegativeBase():
    x = Variable(-5)
    c = Constant(2)
    z = Power(x, c)
    result = z.derive(x)
    assert result.value == approx(25.0)
    assert result.partial == approx(-10.0)

def testPowerWithIntegralExponentAndZeroBase():
    x = Variable(0)
    c = Constant(2)
    z = Power(x, c)
    result = z.derive(x)
    assert result.value == approx(0.0)
    assert result.partial == approx(0.0)

def testPowerWithNegativeIntegralExponent():
    x = Variable(2)
    c = Constant(-2)
    z = Power(x, c)
    result = z.derive(x)
    assert result.value == approx(0.25)
    assert result.partial == approx(-0.25)

def testPowerWithNegativeIntegralExponentAndNegativeBase():
    x = Variable(-2)
    c = Constant(-2)
    z = Power(x, c)
    result = z.derive(x)
    assert result.value == approx(0.25)
    assert result.partial == approx(0.25)

def testPowerWithNegativeIntegralExponentAndZeroBase():
    x = Variable(0)
    c = Constant(-2)
    z = Power(x, c)
    with raises(ArithmeticException):
        z.derive(x)

### Power

def testPower():
    x = Variable(3.0)
    y = Variable(2.5)
    z = Power(x, y)
    resultForX = z.derive(x)
    assert resultForX.value == approx(15.588457268)
    assert resultForX.partial == approx(12.990381056)
    resultForY = z.derive(y)
    assert resultForY.value == approx(15.588457268)
    assert resultForY.partial == approx(17.125670716)

def testPowerWithNegativeBase():
    x = Variable(-3.0)
    y = Variable(2.5)
    z = Power(x, y)
    with raises(ArithmeticException):
        z.derive(x)
    with raises(ArithmeticException):
        z.derive(y)

def testPowerWithZeroBase():
    x = Variable(0.0)
    y = Variable(2.5)
    z = Power(x, y)
    with raises(ArithmeticException):
        z.derive(x)
    with raises(ArithmeticException):
        z.derive(y)

def testPowerWithNegativeExponent():
    x = Variable(3.0)
    y = Variable(-2.5)
    z = Power(x, y)
    resultForX = z.derive(x)
    assert resultForX.value == approx(0.0641500299)
    assert resultForX.partial == approx(-0.0534583582)
    resultForY = z.derive(y)
    assert resultForY.value == approx(0.0641500299)
    assert resultForY.partial == approx(0.0704760111)

def testPowerWithZeroExponent():
    x = Variable(3.0)
    y = Variable(0.0)
    z = Power(x, y)
    resultForX = z.derive(x)
    assert resultForX.value == approx(1.0)
    assert resultForX.partial == approx(0.0)
    resultForY = z.derive(y)
    assert resultForY.value == approx(1.0)
    assert resultForY.partial == approx(1.0986122886)

def testPowerWithZeroBaseAndZeroExponent():
    x = Variable(0.0)
    y = Variable(0.0)
    z = Power(x, y)
    with raises(ArithmeticException):
        z.derive(x)
    with raises(ArithmeticException):
        z.derive(y)

### Polynomials

def testPolynomialOfOneVariable():
    x = Variable(2)
    z = x * x - Constant(6) * x + Constant(4)
    result = z.derive(x)
    assert result.value == -4
    assert result.partial == -2

def testPolynomialOfTwoVariables():
    x = Variable(2)
    y = Variable(3)
    z = x * (x + y) - Constant(5) * y * y
    resultForX = z.derive(x)
    resultForY = z.derive(y)
    assert resultForX.value == -35
    assert resultForX.partial == 7
    assert resultForY.value == -35
    assert resultForY.partial == -28

def testPolynomialOfThreeVariables():
    w = Variable(2)
    x = Variable(3)
    y = Variable(4)
    z = w * w + Constant(5) * w * x * x - w * x * y
    resultForW = z.derive(w)
    resultForX = z.derive(x)
    resultForY = z.derive(y)
    assert resultForW.value == 70
    assert resultForW.partial == 37
    assert resultForX.value == 70
    assert resultForX.partial == 52
    assert resultForY.value == 70
    assert resultForY.partial == -6

### Other

def testCompositeFunction():
    x = Variable(2)
    z = NaturalExponential(x ** Constant(2))
    result = z.derive(x)
    assert result.value == approx(54.598150033)
    assert result.partial == approx(218.392600132)

def testExpressionReuse():
    x = Variable(2)
    w = x ** Constant(2)
    z = (w + Constant(1)) / w
    result = z.derive(x)
    assert result.value == approx(1.25)
    assert result.partial == approx(-0.25)
