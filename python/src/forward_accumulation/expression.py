from __future__ import annotations
from abc import ABC, abstractmethod
import math
from src.forward_accumulation.custom_types import numeric
from src.forward_accumulation.value_and_partial import ValueAndPartial

# !!! should I be worried about expressions like y / (x - x) ?
# !!! how do I want to handle compound constant expressions?

class Expression(ABC):
    @abstractmethod
    def evaluateAndDerive(
        self: Expression,
        variable: Variable     # the variable with which we are differentiating with respect to
    ) -> ValueAndPartial:
        raise Exception("concrete classes derived from Expression must implement evaluateAndDerive()")

    ## Operations ##

    def __neg__(
        self: Expression
    ) -> Negation:
        return Negation(self)

    def __add__(
        self: Expression,
        other: Expression
    ) -> Plus:
        return Plus(self, other)

    def __sub__(
        self: Expression,
        other: Expression
    ) -> Minus:
        return Minus(self, other)

    def __mul__(
        self: Expression,
        other: Expression
    ) -> Multiply:
        return Multiply(self, other)

    def __truediv__(
        self: Expression,
        other: Expression
    ) -> Divide:
        return Divide(self, other)

    def __pow__(
        self: Expression,
        other: Expression
    ) -> PowerWithIntegralExponent | Power:
        # !!! what if other isnt a Constant but evaluates to a constant?
        if isinstance(other, Constant) and isinstance(other.value, int):
            return PowerWithIntegralExponent(self, other)
        else:
            return Power(self, other)

class Constant(Expression):
    def __init__(
        self: Constant,
        value: numeric
    ) -> None:
        self.value = value

    def evaluateAndDerive(
        self: Constant,
        variable: Variable
    ) -> ValueAndPartial:
        return ValueAndPartial(self.value, 0)

class Variable(Expression):
    def __init__(
        self: Variable,
        value: numeric
    ) -> None:
        self.value = value

    def evaluateAndDerive(
        self: Variable,
        variable: Variable
    ) -> ValueAndPartial:
        partial = 1 if self == variable else 0
        return ValueAndPartial(self.value, partial)

class Negation(Expression):
    def __init__(
        self: Negation,
        a: Expression
    ) -> None:
        self.a = a

    def evaluateAndDerive(
        self: Negation,
        variable: Variable
    ) -> ValueAndPartial:
        aValue, aPartial = self.a.evaluateAndDerive(variable).toPair()
        # d(-u) = -du
        return ValueAndPartial(-aValue, -aPartial)

class Reciprocal(Expression):
    def __init__(
        self: Reciprocal,
        a: Expression
    ) -> None:
        self.a = a

    def evaluateAndDerive(
        self: Reciprocal,
        variable: Variable
    ) -> ValueAndPartial:
        aValue, aPartial = self.a.evaluateAndDerive(variable).toPair()
        if aValue == 0:
            raise Exception("cannot divide by zero")
        resultValue = 1 / aValue
        # d(1 / u) = (-1 / u ** 2) * du
        resultPartial = - aPartial * (resultValue ** 2)
        return ValueAndPartial(resultValue, resultPartial)

class NaturalExponential(Expression):
    def __init__(
        self: NaturalExponential,
        a: Expression
    ) -> None:
        self.a = a

    def evaluateAndDerive(
        self: NaturalExponential,
        variable: Variable
    ) -> ValueAndPartial:
        aValue, aPartial = self.a.evaluateAndDerive(variable).toPair()
        resultValue = math.e ** aValue
        # d(e ** v) = e ** v * dv
        resultPartial = resultValue * aPartial
        return ValueAndPartial(resultValue, resultPartial)

class NaturalLogarithm(Expression):
    def __init__(
        self: NaturalLogarithm,
        a: Expression
    ) -> None:
        self.a = a

    def evaluateAndDerive(
        self: NaturalLogarithm,
        variable: Variable
    ) -> ValueAndPartial:
        aValue, aPartial = self.a.evaluateAndDerive(variable).toPair()
        if aValue <= 0:
            raise Exception("can only take the log of a positive number")
        # d(ln(u)) = (1 / u) * du
        return ValueAndPartial(
            math.log(aValue),
            aPartial / aValue
        )

class Sine(Expression):
    def __init__(
        self: Sine,
        a: Expression
    ) -> None:
        self.a = a

    def evaluateAndDerive(
        self: Sine,
        variable: Variable
    ) -> ValueAndPartial:
        aValue, aPartial = self.a.evaluateAndDerive(variable).toPair()
        # d(sin(u)) = cos(u) * du
        return ValueAndPartial(
            math.sin(aValue),
            math.cos(aValue) * aPartial
        )

class Cosine(Expression):
    def __init__(
        self: Cosine,
        a: Expression
    ) -> None:
        self.a = a

    def evaluateAndDerive(
        self: Cosine,
        variable: Variable
    ) -> ValueAndPartial:
        aValue, aPartial = self.a.evaluateAndDerive(variable).toPair()
        # d(cos(u)) = - sin(u) * du
        return ValueAndPartial(
            math.cos(aValue),
            - math.sin(aValue) * aPartial
        )

class Plus(Expression):
    def __init__(
        self: Plus,
        a: Expression,
        b: Expression
    ) -> None:
        self.a = a
        self.b = b

    def evaluateAndDerive(
        self: Plus,
        variable: Variable
    ) -> ValueAndPartial:
        aValue, aPartial = self.a.evaluateAndDerive(variable).toPair()
        bValue, bPartial = self.b.evaluateAndDerive(variable).toPair()
        # d(u + v) = du + dv
        return ValueAndPartial(
            aValue + bValue,
            aPartial + bPartial
        )

class Minus(Expression):
    def __init__(
        self: Minus,
        a: Expression,
        b: Expression
    ) -> None:
        self.a = a
        self.b = b

    def evaluateAndDerive(
        self: Minus,
        variable: Variable
    ) -> ValueAndPartial:
        aValue, aPartial = self.a.evaluateAndDerive(variable).toPair()
        bValue, bPartial = self.b.evaluateAndDerive(variable).toPair()
        # d(u - v) = du - dv
        return ValueAndPartial(
            aValue - bValue,
            aPartial - bPartial
        )

class Multiply(Expression):
    def __init__(
        self: Multiply,
        a: Expression,
        b: Expression
    ) -> None:
        self.a = a
        self.b = b

    def evaluateAndDerive(
        self: Multiply,
        variable: Variable
    ) -> ValueAndPartial:
        aValue, aPartial = self.a.evaluateAndDerive(variable).toPair()
        bValue, bPartial = self.b.evaluateAndDerive(variable).toPair()
        # d(u * v) = v * du + u * dv
        return ValueAndPartial(
            aValue * bValue,
            bValue * aPartial + aValue * bPartial
        )

class Divide(Expression):
    def __init__(
        self: Divide,
        a: Expression,
        b: Expression
    ) -> None:
        self.a = a
        self.b = b

    def evaluateAndDerive(
        self: Divide,
        variable: Variable
    ) -> ValueAndPartial:
        aValue, aPartial = self.a.evaluateAndDerive(variable).toPair()
        bValue, bPartial = self.b.evaluateAndDerive(variable).toPair()
        if bValue == 0:
            raise Exception("cannot divide by zero")
        # d(u / v) = (1 / v) * du - (u / v ** 2) * dv
        return ValueAndPartial(
            aValue / bValue,
            (bValue * aPartial - aValue * bPartial) / bValue ** 2
        )

# When we have an integer in the exponent, we can support negative bases
class PowerWithIntegralExponent(Expression):
    def __init__(
        self: PowerWithIntegralExponent,
        a: Expression,
        b: Constant
    ) -> None:
        # !!! we expect b to be a integral Constant
        self.a = a
        self.b = b

    def evaluateAndDerive(
        self: PowerWithIntegralExponent,
        variable: Variable
    ) -> ValueAndPartial:
        aValue, aPartial = self.a.evaluateAndDerive(variable).toPair()
        bValue = self.b.value
        if aValue == 0 and bValue <= 0:
            raise Exception("cannot have a base of zero unless the exponent is positive")
        resultValue = aValue ** bValue
        # d(u ** c) = c * u ** (c - 1) * du
        resultPartial = bValue * (aValue ** (bValue - 1)) * aPartial
        return ValueAndPartial(resultValue, resultPartial)

class Power(Expression):
    def __init__(
        self: Power,
        a: Expression,
        b: Expression
    ) -> None:
        self.a = a
        self.b = b

    def evaluateAndDerive(
        self: Power,
        variable: Variable
    ) -> ValueAndPartial:
        aValue, aPartial = self.a.evaluateAndDerive(variable).toPair()
        bValue, bPartial = self.b.evaluateAndDerive(variable).toPair()
        if aValue <= 0:
            raise Exception("must have a positive base for non-integral exponents")
        resultValue = aValue ** bValue
        # d(u ** v) = v * u ** (v - 1) * du + ln(u) * u ** v * dv
        resultPartial = (
            (bValue * resultValue / aValue) * aPartial +
            math.log(aValue) * resultValue * bPartial
        )
        return ValueAndPartial(resultValue, resultPartial)
