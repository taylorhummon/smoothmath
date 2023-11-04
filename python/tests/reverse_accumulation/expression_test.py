from pytest import approx, raises
import math
from src.reverse_accumulation.custom_exceptions import DomainException
from src.reverse_accumulation.expression import (
    Constant, Variable,
    Negation, Reciprocal, SquareRoot, Exponential, Logarithm, Sine, Cosine,
    Plus, Minus, Multiply, Divide, Power
)

### Constant

def testConstant():
    c = Constant(7)
    x = Variable("x")
    result = c.derive({ x: 2 })
    assert result.value == 7
    assert result.partialWithRespectTo(x) == 0

### Variable

def testVariable():
    x = Variable("x")
    y = Variable("y")
    result = x.derive({ x: 2, y: 3 })
    assert result.value == 2
    assert result.partialWithRespectTo(x) == 1
    assert result.partialWithRespectTo(y) == 0

### Negation

def testNegation():
    x = Variable("x")
    z = Negation(x)
    result = z.derive({ x: 2 })
    assert result.value == -2
    assert result.partialWithRespectTo(x) == -1

def testNegationComposition():
    x = Variable("x")
    z = Negation(Constant(2) * x + Constant(1))
    result = z.derive({ x: 3 })
    assert result.value == -7
    assert result.partialWithRespectTo(x) == -2

### Reciprocal

def testReciprocal():
    x = Variable("x")
    z = Reciprocal(x)
    result = z.derive({ x: 2 })
    assert result.value == approx(0.5)
    assert result.partialWithRespectTo(x) == approx(-0.25)
    with raises(DomainException):
        z.derive({ x: 0 })
    result = z.derive({ x: -1 })
    assert result.value == approx(-1)
    assert result.partialWithRespectTo(x) == approx(-1)

def testReciprocalComposition():
    x = Variable("x")
    z = Reciprocal(Constant(2) * x - Constant(4))
    result = z.derive({ x: 3 })
    assert result.value == approx(0.5)
    assert result.partialWithRespectTo(x) == approx(-0.5)

### Square Root

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

###  Exponential

def testExponential():
    x = Variable("x")
    z = Exponential(x)
    result = z.derive({ x: 0 })
    assert result.value == approx(1)
    assert result.partialWithRespectTo(x) == approx(1)
    result = z.derive({ x: 1 })
    assert result.value == approx(math.e)
    assert result.partialWithRespectTo(x) == approx(math.e)
    result = z.derive({ x: -1 })
    assert result.value == approx(1 / math.e)
    assert result.partialWithRespectTo(x) == approx(1 / math.e)

def testExponentialComposition():
    x = Variable("x")
    z = Exponential(Constant(2) * x - Constant(6))
    result = z.derive({ x: 3 })
    assert result.value == approx(1)
    assert result.partialWithRespectTo(x) == approx(2)

def testBaseTwoExponential():
    x = Variable("x")
    z = Exponential(x, 2)
    result = z.derive({ x: 0 })
    assert result.value == approx(1)
    assert result.partialWithRespectTo(x) == approx(0.693147180559)
    result = z.derive({ x: 1 })
    assert result.value == approx(2)
    assert result.partialWithRespectTo(x) == approx(1.386294361119)
    result = z.derive({ x: -1 })
    assert result.value == approx(0.5)
    assert result.partialWithRespectTo(x) == approx(0.346573590279)

def testBaseTwoExponentialComposition():
    x = Variable("x")
    z = Exponential(Constant(2) * x - Constant(5), 2)
    result = z.derive({ x: 3 })
    assert result.value == approx(2)
    assert result.partialWithRespectTo(x) == approx(2.77258872223)

###  Logarithm

def testLogarithm():
    x = Variable("x")
    z = Logarithm(x)
    result = z.derive({ x: 1 })
    assert result.value == approx(0)
    assert result.partialWithRespectTo(x) == approx(1)
    result = z.derive({ x: math.e })
    assert result.value == approx(1)
    assert result.partialWithRespectTo(x) == approx(1 / math.e)
    with raises(DomainException):
        z.derive({ x: 0 })
    with raises(DomainException):
        z.derive({ x: -1 })

def testLogarithmComposition():
    x = Variable("x")
    z = Logarithm(Constant(2) * x - Constant(3))
    result = z.derive({ x: 2 })
    assert result.value == approx(0)
    assert result.partialWithRespectTo(x) == approx(2)

def testBaseTwoLogarithm():
    x = Variable("x")
    z = Logarithm(x, 2)
    result = z.derive({ x: 1 })
    assert result.value == approx(0)
    assert result.partialWithRespectTo(x) == approx(1.442695040888)
    result = z.derive({ x: 2 })
    assert result.value == approx(1)
    assert result.partialWithRespectTo(x) == approx(0.721347520444)
    with raises(DomainException):
        z.derive({ x: 0 })
    with raises(DomainException):
        z.derive({ x: -1 })

def testBaseTwoLogarithmComposition():
    x = Variable("x")
    z = Logarithm(Constant(2) * x - Constant(6), 2)
    result = z.derive({ x: 7 })
    assert result.value == approx(3)
    assert result.partialWithRespectTo(x) == approx(0.3606737602222)

### Sine

def testSine():
    theta = Variable("theta")
    z = Sine(theta)
    result = z.derive({ theta: 0 })
    assert result.value == approx(0)
    assert result.partialWithRespectTo(theta) == approx(1)
    result = z.derive({ theta: math.pi / 2 })
    assert result.value == approx(1)
    assert result.partialWithRespectTo(theta) == approx(0)

def testSineComposition():
    theta = Variable("theta")
    z = Sine(Constant(2) * theta)
    result = z.derive({ theta: 0 })
    assert result.value == approx(0)
    assert result.partialWithRespectTo(theta) == approx(2)

### Cosine

def testCosine():
    theta = Variable("theta")
    z = Cosine(theta)
    result = z.derive({ theta: 0 })
    assert result.value == approx(1)
    assert result.partialWithRespectTo(theta) == approx(0)
    result = z.derive({ theta: math.pi / 2 })
    assert result.value == approx(0)
    assert result.partialWithRespectTo(theta) == approx(-1)

def testCosineComposition():
    theta = Variable("theta")
    z = Cosine(Constant(2) * theta)
    result = z.derive({ theta: math.pi / 4 })
    assert result.value == approx(0)
    assert result.partialWithRespectTo(theta) == approx(-2)

### Plus

def testPlus():
    x = Variable("x")
    y = Variable("y")
    z = Plus(x, y)
    result = z.derive({ x: 2, y: 3 })
    assert result.value == approx(5)
    assert result.partialWithRespectTo(x) == approx(1)
    assert result.partialWithRespectTo(y) == approx(1)

def testPlusComposition():
    x = Variable("x")
    y = Variable("y")
    z = Plus(Constant(5) * x, Constant(4) * y)
    result = z.derive({ x: 2, y: 3 })
    assert result.value == approx(22)
    assert result.partialWithRespectTo(x) == approx(5)
    assert result.partialWithRespectTo(y) == approx(4)

### Minus

def testMinus():
    x = Variable("x")
    y = Variable("y")
    z = Minus(x, y)
    result = z.derive({ x: 2, y: 3 })
    assert result.value == approx(-1)
    assert result.partialWithRespectTo(x) == approx(1)
    assert result.partialWithRespectTo(y) == approx(-1)

def testMinusComposition():
    x = Variable("x")
    y = Variable("y")
    z = Minus(Constant(5) * x, Constant(4) * y)
    result = z.derive({ x: 2, y: 3 })
    assert result.value == approx(-2)
    assert result.partialWithRespectTo(x) == approx(5)
    assert result.partialWithRespectTo(y) == approx(-4)

### Multiply

def testMultiply():
    x = Variable("x")
    y = Variable("y")
    z = Multiply(x, y)
    result = z.derive({ x: 2, y: 3 })
    assert result.value == approx(6)
    assert result.partialWithRespectTo(x) == approx(3)
    assert result.partialWithRespectTo(y) == approx(2)

def testMultiplyComposition():
    x = Variable("x")
    y = Variable("y")
    z = Multiply(Constant(5) * x, y - Constant(1))
    result = z.derive({ x: 2, y: 3 })
    assert result.value == approx(20)
    assert result.partialWithRespectTo(x) == approx(10)
    assert result.partialWithRespectTo(y) == approx(10)

def testMultiplyByZero():
    x = Variable("x")
    z = Multiply(Constant(0), x)
    result = z.derive({ x: 2 })
    assert result.value == approx(0)
    assert result.partialWithRespectTo(x) == approx(0)

def testMultiplyByZeroDoesntShortCircuit():
    x = Variable("x")
    z = Multiply(Constant(0), Power(Constant(-1), x))
    with raises(DomainException):
        z.derive({ x: 2 })

def testMultiplyByOne():
    x = Variable("x")
    z = Multiply(Constant(1), x)
    result = z.derive({ x: 2 })
    assert result.value == approx(2)
    assert result.partialWithRespectTo(x) == approx(1)

### Divide

def testDivide():
    x = Variable("x")
    y = Variable("y")
    z = Divide(x, y)
    result = z.derive({ x: 5, y: 2 })
    assert result.value == approx(2.5)
    assert result.partialWithRespectTo(x) == approx(0.5)
    assert result.partialWithRespectTo(y) == approx(-1.25)
    with raises(DomainException):
        z.derive({ x: 3, y: 0 })
    with raises(DomainException):
        z.derive({ x: 0, y: 0 })

def testDivideComposition():
    x = Variable("x")
    y = Variable("y")
    z = Divide(Constant(2) * x + Constant(4), Constant(5) * y)
    result = z.derive({ x: 3, y: 1 })
    assert result.value == approx(2)
    assert result.partialWithRespectTo(x) == approx(0.4)
    assert result.partialWithRespectTo(y) == approx(-2)

def testDivideWithConstantNumeratorZero():
    y = Variable("y")
    z = Divide(Constant(0), y)
    result = z.derive({ y: 3 })
    assert result.value == approx(0)
    assert result.partialWithRespectTo(y) == approx(0)
    result = z.derive({ y: 0 })
    assert result.value == approx(0)
    assert result.partialWithRespectTo(y) == approx(0)

def testDivideWithConstantNumeratorZeroComposition():
    y = Variable("y")
    z = Divide(Constant(0), Constant(2) * y + Constant(4))
    result = z.derive({ y: 3 })
    assert result.value == approx(0)
    assert result.partialWithRespectTo(y) == approx(0)

def testDivideWithConstantNumeratorZeroDoesntShortCircuit():
    y = Variable("y")
    z = Divide(Constant(0), Logarithm(y))
    with raises(DomainException):
        z.derive({ y: 0 })

def testDivideWithConstantDenominatorOne():
    x = Variable("x")
    z = Divide(x, Constant(1))
    result = z.derive({ x: 3 })
    assert result.value == approx(3)
    assert result.partialWithRespectTo(x) == approx(1)
    result = z.derive({ x: 0 })
    assert result.value == approx(0)
    assert result.partialWithRespectTo(x) == approx(1)

def testDivideWithConstantDenominatorZero():
    x = Variable("x")
    z = Divide(x, Constant(0))
    with raises(DomainException):
        z.derive({ x: 3 })
    with raises(DomainException):
        z.derive({ x: 0 })

### Power

def testPower():
    x = Variable("x")
    y = Variable("y")
    z = Power(x, y)
    result = z.derive({ x: 3, y: 2.5 })
    assert result.value == approx(15.588457268)
    assert result.partialWithRespectTo(x) == approx(12.990381056)
    assert result.partialWithRespectTo(y) == approx(17.125670716)
    result = z.derive({ x: 3, y: 0 })
    assert result.value == approx(1)
    assert result.partialWithRespectTo(x) == approx(0)
    assert result.partialWithRespectTo(y) == approx(1.0986122886)
    result = z.derive({ x: 3, y: -2.5 })
    assert result.value == approx(0.0641500299)
    assert result.partialWithRespectTo(x) == approx(-0.0534583582)
    assert result.partialWithRespectTo(y) == approx(0.0704760111)
    with raises(DomainException):
        z.derive({ x: 0, y: 2.5 })
    with raises(DomainException):
        z.derive({ x: 0, y: 0 })
    with raises(DomainException):
        z.derive({ x: 0, y: -2.5 })
    with raises(DomainException):
        z.derive({ x: -3, y: 2.5 })
    with raises(DomainException):
        z.derive({ x: -3, y: 0 })
    with raises(DomainException):
        z.derive({ x: -3, y: -2.5 })

def testPowerComposition():
    x = Variable("x")
    y = Variable("y")
    z = Power(Constant(2) * x, Constant(3) * y)
    result = z.derive({ x: 1, y: 1 })
    assert result.value == approx(8)
    assert result.partialWithRespectTo(x) == approx(24)
    assert result.partialWithRespectTo(y) == approx(16.63553233343)

def testPowerWithConstantBaseOne():
    y = Variable("y")
    z = Power(Constant(1), y)
    result = z.derive({ y: 3 })
    assert result.value == approx(1)
    assert result.partialWithRespectTo(y) == approx(0)
    result = z.derive({ y: 0 })
    assert result.value == approx(1)
    assert result.partialWithRespectTo(y) == approx(0)
    result = z.derive({ y: -5 })
    assert result.value == approx(1)
    assert result.partialWithRespectTo(y) == approx(0)

def testPowerWithConstantBaseOneDoesntShortCircuit():
    x = Variable("x")
    z = Power(Constant(1), SquareRoot(x))
    with raises(DomainException):
        z.derive({ x: -1 })

def testPowerWithConstantBaseZero():
    y = Variable("y")
    z = Power(Constant(0), y)
    with raises(DomainException):
        z.derive({ y: 3 })
    with raises(DomainException):
        z.derive({ y: 0 })
    with raises(DomainException):
        z.derive({ y: -5 })

def testPowerWithConstantBaseNegativeOne():
    y = Variable("y")
    z = Power(Constant(-1), y)
    with raises(DomainException):
        z.derive({ y: 3 })
    with raises(DomainException):
        z.derive({ y: 0 })
    with raises(DomainException):
        z.derive({ y: -5 })

def testPowerWithConstantExponentTwo():
    x = Variable("x")
    z = Power(x, Constant(2))
    result = z.derive({ x: 3 })
    assert result.value == approx(9)
    assert result.partialWithRespectTo(x) == approx(6)
    result = z.derive({ x: 0 })
    assert result.value == approx(0)
    assert result.partialWithRespectTo(x) == approx(0)
    result = z.derive({ x: -5 })
    assert result.value == approx(25)
    assert result.partialWithRespectTo(x) == approx(-10)

def testPowerWithConstantExponentTwoComposition():
    x = Variable("x")
    z = Power(Constant(3) * x - Constant(1), Constant(2))
    result = z.derive({ x: 1 })
    assert result.value == approx(4)
    assert result.partialWithRespectTo(x) == approx(12)

def testPowerWithConstantExponentOne():
    x = Variable("x")
    z = Power(x, Constant(1))
    result = z.derive({ x: 3 })
    assert result.value == approx(3)
    assert result.partialWithRespectTo(x) == approx(1)
    result = z.derive({ x: 0 })
    assert result.value == approx(0)
    assert result.partialWithRespectTo(x) == approx(1)
    result = z.derive({ x: -5 })
    assert result.value == approx(-5)
    assert result.partialWithRespectTo(x) == approx(1)

def testPowerWithConstantExponentOneComposition():
    x = Variable("x")
    z = Power(Constant(3) * x - Constant(1), Constant(1))
    result = z.derive({ x: 1 })
    assert result.value == approx(2)
    assert result.partialWithRespectTo(x) == approx(3)

def testPowerWithConstantExponentZero():
    x = Variable("x")
    z = Power(x, Constant(0))
    result = z.derive({ x: 3 })
    assert result.value == approx(1)
    assert result.partialWithRespectTo(x) == approx(0)
    result = z.derive({ x: 0 })
    assert result.value == approx(1)
    assert result.partialWithRespectTo(x) == approx(0)
    result = z.derive({ x: -5 })
    assert result.value == approx(1)
    assert result.partialWithRespectTo(x) == approx(0)

def testPowerWithConstantExponentZeroComposition():
    x = Variable("x")
    z = Power(Constant(3) * x - Constant(1), Constant(0))
    result = z.derive({ x: 1 })
    assert result.value == approx(1)
    assert result.partialWithRespectTo(x) == approx(0)

def testPowerWithConstantExponentZeroDoesntShortCircuit():
    x = Variable("x")
    z = Power(Logarithm(x), Constant(0))
    with raises(DomainException):
        z.derive({ x: 0 })

def testPowerWithConstantExponentNegativeOne():
    x = Variable("x")
    z = Power(x, Constant(-1))
    result = z.derive({ x: 2 })
    assert result.value == approx(0.5)
    assert result.partialWithRespectTo(x) == approx(-0.25)
    with raises(DomainException):
        z.derive({ x: 0 })
    result = z.derive({ x: -5 })
    assert result.value == approx(-0.2)
    assert result.partialWithRespectTo(x) == approx(-0.04)

def testPowerWithConstantExponentNegativeOneComposition():
    x = Variable("x")
    z = Power(Constant(3) * x - Constant(1), Constant(-1))
    result = z.derive({ x: 1 })
    assert result.value == approx(0.5)
    assert result.partialWithRespectTo(x) == approx(-0.75)

def testPowerWithConstantExponentNegativeTwo():
    x = Variable("x")
    z = Power(x, Constant(-2))
    result = z.derive({ x: 2 })
    assert result.value == approx(0.25)
    assert result.partialWithRespectTo(x) == approx(-0.25)
    with raises(DomainException):
        z.derive({ x: 0 })
    result = z.derive({ x: -5 })
    assert result.value == approx(0.04)
    assert result.partialWithRespectTo(x) == approx(0.016)

def testPowerWithConstantExponentNegativeTwoComposition():
    x = Variable("x")
    z = Power(Constant(3) * x - Constant(1), Constant(-2))
    result = z.derive({ x: 1 })
    assert result.value == approx(0.25)
    assert result.partialWithRespectTo(x) == approx(-0.75)

def testPowerWithExponentMadeFromAddingConstants():
    x = Variable("x")
    z = Power(x, Constant(1) + Constant(1))
    result = z.derive({ x: 3 })
    assert result.value == approx(9)
    assert result.partialWithRespectTo(x) == approx(6)
    result = z.derive({ x: 0 })
    assert result.value == approx(0)
    assert result.partialWithRespectTo(x) == approx(0)
    result = z.derive({ x: -5 })
    assert result.value == approx(25)
    assert result.partialWithRespectTo(x) == approx(-10)

def testPowerWhereExponentIsAnIntegerRepresentedAsAFloat():
    x = Variable("x")
    z = Power(x, Constant(2.0))
    result = z.derive({ x: -5 })
    assert result.value == approx(25)
    assert result.partialWithRespectTo(x) == approx(-10)

### Polynomials

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

### Other

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
