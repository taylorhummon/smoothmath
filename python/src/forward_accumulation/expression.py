from __future__ import annotations
from abc import ABC, abstractmethod
import math
from src.forward_accumulation.custom_types import numeric, VariableValues
from src.forward_accumulation.custom_exceptions import MathException
from src.forward_accumulation.result import Result

# !!! improve test coverage
# !!! how big a problem are indeterminate forms?
# !!! do we want a lhopital or anything?
# !!! how badly do things go due to floating point imprecision?

class Expression(ABC):
    @abstractmethod
    def derive(
        self: Expression,
        variableValues: VariableValues,
        withRespectTo: Variable
    ) -> Result:
        raise Exception("concrete classes derived from Expression must implement derive()")

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
    ) -> Power:
        return Power(self, other)

class Constant(Expression):
    def __init__(
        self: Constant,
        value: numeric
    ) -> None:
        self.value = value

    def derive(
        self: Constant,
        variableValues: VariableValues,
        withRespectTo: Variable
    ) -> Result:
        return Result(self.value, 0, set())

class Variable(Expression):
    def __init__(
        self: Variable
    ) -> None:
        pass

    def derive(
        self: Variable,
        variableValues: VariableValues,
        withRespectTo: Variable
    ) -> Result:
        value = variableValues.get(self, None)
        if value is None:
            raise Exception("variableValues missing a value for a variable")
        partial = 1 if self == withRespectTo else 0
        return Result(value, partial, { self })

class Negation(Expression):
    def __init__(
        self: Negation,
        a: Expression
    ) -> None:
        self.a = a

    def derive(
        self: Negation,
        variableValues: VariableValues,
        withRespectTo: Variable
    ) -> Result:
        aValue, aPartial, aDependsOn = self.a.derive(variableValues, withRespectTo).toTriple()
        # d(-u) = -du
        return Result(-aValue, -aPartial, aDependsOn)

class Reciprocal(Expression):
    def __init__(
        self: Reciprocal,
        a: Expression
    ) -> None:
        self.a = a

    def derive(
        self: Reciprocal,
        variableValues: VariableValues,
        withRespectTo: Variable
    ) -> Result:
        aValue, aPartial, aDependsOn = self.a.derive(variableValues, withRespectTo).toTriple()
        if aValue == 0:
            raise MathException("1 / x at x = 0")
        resultValue = 1 / aValue
        # d(1 / u) = (-1 / u ** 2) * du
        resultPartial = - aPartial * (resultValue ** 2)
        return Result(resultValue, resultPartial, aDependsOn)

class SquareRoot(Expression):
    def __init__(
        self: SquareRoot,
        a: Expression
    ) -> None:
        self.a = a

    def derive(
        self: SquareRoot,
        variableValues: VariableValues,
        withRespectTo: Variable
    ) -> Result:
        aValue, aPartial, aDependsOn = self.a.derive(variableValues, withRespectTo).toTriple()
        if aValue == 0:
            raise MathException("sqrt(x) at x = 0")
        elif aValue < 0:
            raise MathException("sqrt(x) for x < 0")
        resultValue = math.sqrt(aValue)
        # d(sqrt(v)) = (1 / (2 sqrt(v))) * dv
        resultPartial = (1 / (2 * resultValue)) * aPartial
        return Result(resultValue, resultPartial, aDependsOn)

class NaturalExponential(Expression):
    def __init__(
        self: NaturalExponential,
        a: Expression
    ) -> None:
        self.a = a

    def derive(
        self: NaturalExponential,
        variableValues: VariableValues,
        withRespectTo: Variable
    ) -> Result:
        aValue, aPartial, aDependsOn = self.a.derive(variableValues, withRespectTo).toTriple()
        resultValue = math.e ** aValue
        # d(e ** v) = e ** v * dv
        resultPartial = resultValue * aPartial
        return Result(resultValue, resultPartial, aDependsOn)

class NaturalLogarithm(Expression):
    def __init__(
        self: NaturalLogarithm,
        a: Expression
    ) -> None:
        self.a = a

    def derive(
        self: NaturalLogarithm,
        variableValues: VariableValues,
        withRespectTo: Variable
    ) -> Result:
        aValue, aPartial, aDependsOn = self.a.derive(variableValues, withRespectTo).toTriple()
        if aValue == 0:
            raise MathException("ln(x) at x = 0")
        elif aValue < 0:
            raise MathException("ln(x) for x < 0")
        # d(ln(u)) = (1 / u) * du
        return Result(
            math.log(aValue),
            aPartial / aValue,
            aDependsOn
        )

class Sine(Expression):
    def __init__(
        self: Sine,
        a: Expression
    ) -> None:
        self.a = a

    def derive(
        self: Sine,
        variableValues: VariableValues,
        withRespectTo: Variable
    ) -> Result:
        aValue, aPartial, aDependsOn = self.a.derive(variableValues, withRespectTo).toTriple()
        # d(sin(u)) = cos(u) * du
        return Result(
            math.sin(aValue),
            math.cos(aValue) * aPartial,
            aDependsOn
        )

class Cosine(Expression):
    def __init__(
        self: Cosine,
        a: Expression
    ) -> None:
        self.a = a

    def derive(
        self: Cosine,
        variableValues: VariableValues,
        withRespectTo: Variable
    ) -> Result:
        aValue, aPartial, aDependsOn = self.a.derive(variableValues, withRespectTo).toTriple()
        # d(cos(u)) = - sin(u) * du
        return Result(
            math.cos(aValue),
            - math.sin(aValue) * aPartial,
            aDependsOn
        )

class Plus(Expression):
    def __init__(
        self: Plus,
        a: Expression,
        b: Expression
    ) -> None:
        self.a = a
        self.b = b

    def derive(
        self: Plus,
        variableValues: VariableValues,
        withRespectTo: Variable
    ) -> Result:
        aValue, aPartial, aDependsOn = self.a.derive(variableValues, withRespectTo).toTriple()
        bValue, bPartial, bDependsOn = self.b.derive(variableValues, withRespectTo).toTriple()
        # d(u + v) = du + dv
        return Result(
            aValue + bValue,
            aPartial + bPartial,
            aDependsOn | bDependsOn
        )

class Minus(Expression):
    def __init__(
        self: Minus,
        a: Expression,
        b: Expression
    ) -> None:
        self.a = a
        self.b = b

    def derive(
        self: Minus,
        variableValues: VariableValues,
        withRespectTo: Variable
    ) -> Result:
        aValue, aPartial, aDependsOn = self.a.derive(variableValues, withRespectTo).toTriple()
        bValue, bPartial, bDependsOn = self.b.derive(variableValues, withRespectTo).toTriple()
        # d(u - v) = du - dv
        return Result(
            aValue - bValue,
            aPartial - bPartial,
            aDependsOn | bDependsOn
        )

class Multiply(Expression):
    def __init__(
        self: Multiply,
        a: Expression,
        b: Expression
    ) -> None:
        self.a = a
        self.b = b

    def derive(
        self: Multiply,
        variableValues: VariableValues,
        withRespectTo: Variable
    ) -> Result:
        aValue, aPartial, aDependsOn = self.a.derive(variableValues, withRespectTo).toTriple()
        bValue, bPartial, bDependsOn = self.b.derive(variableValues, withRespectTo).toTriple()
        # d(u * v) = v * du + u * dv
        return Result(
            aValue * bValue,
            bValue * aPartial + aValue * bPartial,
            aDependsOn | bDependsOn
        )

class Divide(Expression):
    def __init__(
        self: Divide,
        a: Expression,
        b: Expression
    ) -> None:
        self.a = a
        self.b = b

    def derive(
        self: Divide,
        variableValues: VariableValues,
        withRespectTo: Variable
    ) -> Result:
        aValue, aPartial, aDependsOn = self.a.derive(variableValues, withRespectTo).toTriple()
        bValue, bPartial, bDependsOn = self.b.derive(variableValues, withRespectTo).toTriple()
        if bValue == 0:
            if aValue == 0:
                raise MathException("x / y at (x, y) = (0, 0)")
            else:
                raise MathException("x / y with x != 0 and y = 0")

        # d(u / v) = (1 / v) * du - (u / v ** 2) * dv
        return Result(
            aValue / bValue,
            (bValue * aPartial - aValue * bPartial) / bValue ** 2,
            aDependsOn | bDependsOn
        )

class Power(Expression):
    def __init__(
        self: Power,
        a: Expression,
        b: Expression
    ) -> None:
        self.a = a
        self.b = b

    # For a power a ** b, there are two over-arching cases we work with:
    # (I) the exponent, b, can be determined to be a constant integer
    #     e.g. a ** 2, a ** 3, or a ** (-1)
    # (II) otherwise
    #     e.g. e ** b, or 3 ** b, a ** b,
    # In case (I), we support negative bases. In case (II), we only support positive bases.

    def derive(
        self: Power,
        variableValues: VariableValues,
        withRespectTo: Variable
    ) -> Result:
        aValue, aPartial, aDependsOn = self.a.derive(variableValues, withRespectTo).toTriple()
        bValue, bPartial, bDependsOn = self.b.derive(variableValues, withRespectTo).toTriple()
        resultDependsOn = aDependsOn | bDependsOn
        if (withRespectTo not in bDependsOn) and bValue.is_integer(): # CASE I: has constant integer exponent
            if bValue >= 2:
                resultValue = aValue ** bValue
                # d(u ** c) = c * u ** (c - 1) * du
                resultPartial = bValue * (aValue ** (bValue - 1)) * aPartial
                return Result(resultValue, resultPartial, resultDependsOn)
            elif bValue == 1:
                resultValue = aValue
                # d(u ** 1) = 1 * du
                resultPartial = aPartial
                return Result(resultValue, resultPartial, resultDependsOn)
            elif bValue == 0:
                if aValue == 0:
                    raise MathException("x ** 0 at x = 0")
                resultValue = 1
                # d(u ** 0) = 0 * du
                resultPartial = 0
                return Result(resultValue, resultPartial, resultDependsOn)
            else: # bValue <= -1:
                if aValue == 0:
                    raise MathException("x ** c at x = 0 and c is a negative integer")
                resultValue = aValue ** bValue
                # d(u ** c) = c * u ** (c - 1) * du
                resultPartial = (bValue * resultValue / aValue) * aPartial
                return Result(resultValue, resultPartial, resultDependsOn)
        else: # CASE II: does not have a constant integer exponent
            if aValue > 0:
                resultValue = aValue ** bValue
                # d(u ** v) = v * u ** (v - 1) * du + ln(u) * u ** v * dv
                resultPartial = (
                    (bValue * resultValue / aValue) * aPartial +
                    math.log(aValue) * resultValue * bPartial
                )
                return Result(resultValue, resultPartial, resultDependsOn)
            elif aValue == 0:
                raise MathException("x ** y at x = 0")
            else: # aValue < 0:
                raise MathException("x ** y at x < 0")
