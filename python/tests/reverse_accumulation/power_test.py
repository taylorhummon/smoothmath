from pytest import approx, raises
from src.reverse_accumulation.custom_exceptions import DomainException
from src.reverse_accumulation.constant import Constant
from src.reverse_accumulation.variable import Variable
from src.reverse_accumulation.square_root import SquareRoot
from src.reverse_accumulation.logarithm import Logarithm
from src.reverse_accumulation.power import Power

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
