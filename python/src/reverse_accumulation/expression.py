from __future__ import annotations
from abc import ABC, abstractmethod
import math
from src.reverse_accumulation.custom_types import numeric
from src.reverse_accumulation.computed_partials import ComputedPartials

class Expression(ABC):
    def __init__(
        self: Expression
    ) -> None:
        self._value : numeric | None
        self._value = None

    ## Evaluation ##

    def evaluate(
        self: Expression
    ) -> numeric:
        if self._value is None:
            self._value = self._evaluate()
        return self._value

    @abstractmethod
    def _evaluate(
        self: Expression
    ) -> numeric:
        raise Exception("concrete classes derived from Expression must implement _evaluate()")

    ## Derivation ##

    def derive(
        self: Expression
    ) -> ComputedPartials:
        computedPartials = ComputedPartials()
        self._derive(computedPartials, 1)
        return computedPartials

    @abstractmethod
    def _derive(
        self: Expression,
        computedPartials: ComputedPartials,
        seed: numeric
    ) -> None:
        raise Exception("concrete classes derived from Expression must implement _derive()")

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
        if isinstance(other, Constant) and isinstance(other.evaluate(), int):
            return PowerWithIntegralExponent(self, other)
        else:
            return Power(self, other)

### Nullary Expressions ###

class NullaryExpression(Expression):
    def __init__(
        self: NullaryExpression
    ) -> None:
        super().__init__()

class Constant(NullaryExpression):
    def __init__(
        self: Constant,
        value: numeric
    ) -> None:
        super().__init__()
        self._valueFromInit = value

    def _evaluate(
        self: Constant
    ) -> numeric:
        return self._valueFromInit

    def _derive(
        self: Constant,
        computedPartials: ComputedPartials,
        seed: numeric
    ) -> None:
        pass

class Variable(NullaryExpression):
    def __init__(
        self: Variable,
        value: numeric
    ) -> None:
        super().__init__()
        self._valueFromInit = value

    def _evaluate(
        self: Variable
    ) -> numeric:
        return self._valueFromInit

    def _derive(
        self: Variable,
        computedPartials: ComputedPartials,
        seed: numeric
    ) -> None:
        computedPartials.addSeed(self, seed)

### Unary Expressions ###

class UnaryExpression(Expression):
    def __init__(
        self: UnaryExpression,
        a: Expression
    ) -> None:
        super().__init__()
        self.a = a

class Negation(UnaryExpression):
    def __init__(
        self: Negation,
        a: Expression
    ) -> None:
        super().__init__(a)

    def _evaluate(
        self: Negation
    ) -> numeric:
        aValue = self.a.evaluate()
        return - aValue

    def _derive(
        self: Negation,
        computedPartials: ComputedPartials,
        seed: numeric
    ) -> None:
        # d(-u) = -du
        self.a._derive(computedPartials, -seed)

class Reciprocal(UnaryExpression):
    def __init__(
        self: Reciprocal,
        a: Expression
    ) -> None:
        super().__init__(a)

    def _evaluate(
        self: Reciprocal
    ) -> numeric:
        aValue = self.a.evaluate()
        if aValue == 0:
            raise Exception("cannot divide by zero")
        return 1 / aValue

    def _derive(
        self: Reciprocal,
        computedPartials: ComputedPartials,
        seed: numeric
    ) -> None:
        selfValue = self.evaluate()
        # d(1 / u) = (-1 / u ** 2) * du
        self.a._derive(computedPartials, - seed * (selfValue ** 2))

class NaturalExponential(UnaryExpression):
    def __init__(
        self: NaturalExponential,
        a: Expression
    ) -> None:
        super().__init__(a)

    def _evaluate(
        self: NaturalExponential
    ) -> numeric:
        aValue = self.a.evaluate()
        return math.e ** aValue

    def _derive(
        self: NaturalExponential,
        computedPartials: ComputedPartials,
        seed: numeric
    ) -> None:
        selfValue = self.evaluate()
        # d(e ** v) = e ** v * dv
        self.a._derive(computedPartials, seed * selfValue)

class NaturalLogarithm(UnaryExpression):
    def __init__(
        self: NaturalLogarithm,
        a: Expression
    ) -> None:
        super().__init__(a)

    def _evaluate(
        self: NaturalLogarithm
    ) -> numeric:
        aValue = self.a.evaluate()
        if aValue <= 0:
            raise Exception("can only take the log of a positive number")
        return math.log(aValue)

    def _derive(
        self: NaturalLogarithm,
        computedPartials: ComputedPartials,
        seed: numeric
    ) -> None:
        aValue = self.a.evaluate()
        if aValue <= 0:
            raise Exception("can only take the log of a positive number")
        # d(ln(u)) = (1 / u) * du
        self.a._derive(computedPartials, seed / aValue)

class Sine(UnaryExpression):
    def __init__(
        self: Sine,
        a: Expression
    ) -> None:
        super().__init__(a)

    def _evaluate(
        self: Sine
    ) -> numeric:
        aValue = self.a.evaluate()
        return math.sin(aValue)

    def _derive(
        self: Sine,
        computedPartials: ComputedPartials,
        seed: numeric
    ) -> None:
        aValue = self.a.evaluate()
        # d(sin(u)) = cos(u) * du
        self.a._derive(computedPartials, math.cos(aValue) * seed)

class Cosine(UnaryExpression):
    def __init__(
        self: Cosine,
        a: Expression
    ) -> None:
        super().__init__(a)

    def _evaluate(
        self: Cosine
    ) -> numeric:
        aValue = self.a.evaluate()
        return math.cos(aValue)

    def _derive(
        self: Cosine,
        computedPartials: ComputedPartials,
        seed: numeric
    ) -> None:
        aValue = self.a.evaluate()
        # d(cos(u)) = - sin(u) * du
        self.a._derive(computedPartials, - math.sin(aValue) * seed)

### Binary Expressions ###

class BinaryExpression(Expression):
    def __init__(
        self: BinaryExpression,
        a: Expression,
        b: Expression
    ) -> None:
        super().__init__()
        self.a = a
        self.b = b

class Plus(BinaryExpression):
    def __init__(
        self: Plus,
        a: Expression,
        b: Expression
    ) -> None:
        super().__init__(a, b)

    def _evaluate(
        self: Plus
    ) -> numeric:
        aValue = self.a.evaluate()
        bValue = self.b.evaluate()
        return aValue + bValue

    def _derive(
        self: Plus,
        computedPartials: ComputedPartials,
        seed: numeric
    ) -> None:
        # d(u + v) = du + dv
        self.a._derive(computedPartials, seed)
        self.b._derive(computedPartials, seed)

class Minus(BinaryExpression):
    def __init__(
        self: Minus,
        a: Expression,
        b: Expression
    ) -> None:
        super().__init__(a, b)

    def _evaluate(
        self: Minus
    ) -> numeric:
        aValue = self.a.evaluate()
        bValue = self.b.evaluate()
        return aValue - bValue

    def _derive(
        self: Minus,
        computedPartials: ComputedPartials,
        seed: numeric
    ) -> None:
        # d(u - v) = du - dv
        self.a._derive(computedPartials, seed)
        self.b._derive(computedPartials, - seed)

class Multiply(BinaryExpression):
    def __init__(
        self: Multiply,
        a: Expression,
        b: Expression
    ) -> None:
        super().__init__(a, b)

    def _evaluate(
        self: Multiply
    ) -> numeric:
        aValue = self.a.evaluate()
        bValue = self.b.evaluate()
        return aValue * bValue

    def _derive(
        self: Multiply,
        computedPartials: ComputedPartials,
        seed: numeric
    ) -> None:
        aValue = self.a.evaluate()
        bValue = self.b.evaluate()
        # d(u * v) = v * du + u * dv
        self.a._derive(computedPartials, bValue * seed)
        self.b._derive(computedPartials, aValue * seed)

class Divide(BinaryExpression):
    def __init__(
        self: Divide,
        a: Expression,
        b: Expression
    ) -> None:
        super().__init__(a, b)

    def _evaluate(
        self: Divide
    ) -> numeric:
        aValue = self.a.evaluate()
        bValue = self.b.evaluate()
        if bValue == 0:
            raise Exception("cannot divide by zero")
        return aValue / bValue

    def _derive(
        self: Divide,
        computedPartials: ComputedPartials,
        seed: numeric
    ) -> None:
        aValue = self.a.evaluate()
        bValue = self.b.evaluate()
        if bValue == 0:
            raise Exception("cannot divide by zero")
        # d(u / v) = (1 / v) * du - (u / v ^ 2) * dv
        self.a._derive(computedPartials, seed / bValue)
        self.b._derive(computedPartials, - seed * aValue / (bValue ** 2))

# When we have an integer in the exponent, we can support negative bases
class PowerWithIntegralExponent(BinaryExpression):
    def __init__(
        self: PowerWithIntegralExponent,
        a: Expression,
        b: Expression
    ) -> None:
        super().__init__(a, b)

    def _evaluate(
        self: PowerWithIntegralExponent
    ) -> numeric:
        aValue = self.a.evaluate()
        bValue = self.b.evaluate()
        if aValue == 0 and bValue <= 0:
            raise Exception("cannot have a base of zero unless the exponent is positive")
        return aValue ** bValue

    def _derive(
        self: PowerWithIntegralExponent,
        computedPartials: ComputedPartials,
        seed: numeric
    ) -> None:
        aValue = self.a.evaluate()
        bValue = self.b.evaluate()
        if aValue == 0 and bValue <= 0:
            raise Exception("cannot have a base of zero unless the exponent is positive")
        # d(u ** c) = c * u ** (c - 1) * du
        self.a._derive(computedPartials, seed * bValue * (aValue ** (bValue - 1)))

class Power(BinaryExpression):
    def __init__(
        self: Power,
        a: Expression,
        b: Expression
    ) -> None:
        super().__init__(a, b)

    def _evaluate(
        self: Power
    ) -> numeric:
        aValue = self.a.evaluate()
        bValue = self.b.evaluate()
        if aValue <= 0:
            raise Exception("must have a positive base for non-integral exponents")
        return aValue ** bValue

    def _derive(
        self: Power,
        computedPartials: ComputedPartials,
        seed: numeric
    ) -> None:
        aValue = self.a.evaluate()
        bValue = self.b.evaluate()
        selfValue = self.evaluate()
        # d(u ** v) = v * u ** (v - 1) * du + ln(u) * u ** v * dv
        self.a._derive(computedPartials, seed * bValue * (aValue ** (bValue - 1)))
        self.b._derive(computedPartials, seed * math.log(aValue) * selfValue)
