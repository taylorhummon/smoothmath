from __future__ import annotations
from abc import ABC, abstractmethod
import math
from src.forward_accumulation.custom_types import numeric
from src.forward_accumulation.custom_exceptions import ValueUndefinedException, IndeterminateFormException
from src.forward_accumulation.result import Result

# !!! square root
# !!! consider providing a VariableValues dict instead of providing Variables values on creation
# !!! improve test coverage
# !!! how big a problem are indeterminate forms?
# !!! do we want a lhopital or anything?
# !!! how badly do things go due to floating point imprecision?

class Expression(ABC):
    @abstractmethod
    def derive(
        self: Expression,
        variable: Variable     # the variable with which we are differentiating with respect to
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
        variable: Variable
    ) -> Result:
        return Result(self.value, 0, set())

class Variable(Expression):
    def __init__(
        self: Variable,
        value: numeric
    ) -> None:
        self.value = value

    def derive(
        self: Variable,
        variable: Variable
    ) -> Result:
        partial = 1 if self == variable else 0
        return Result(self.value, partial, { self })

class Negation(Expression):
    def __init__(
        self: Negation,
        a: Expression
    ) -> None:
        self.a = a

    def derive(
        self: Negation,
        variable: Variable
    ) -> Result:
        aValue, aPartial, aDependsOn = self.a.derive(variable).toTriple()
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
        variable: Variable
    ) -> Result:
        aValue, aPartial, aDependsOn = self.a.derive(variable).toTriple()
        if aValue == 0:
            raise ValueUndefinedException("1 / 0")
        resultValue = 1 / aValue
        # d(1 / u) = (-1 / u ** 2) * du
        resultPartial = - aPartial * (resultValue ** 2)
        return Result(resultValue, resultPartial, aDependsOn)

class NaturalExponential(Expression):
    def __init__(
        self: NaturalExponential,
        a: Expression
    ) -> None:
        self.a = a

    def derive(
        self: NaturalExponential,
        variable: Variable
    ) -> Result:
        aValue, aPartial, aDependsOn = self.a.derive(variable).toTriple()
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
        variable: Variable
    ) -> Result:
        aValue, aPartial, aDependsOn = self.a.derive(variable).toTriple()
        if aValue == 0:
            raise ValueUndefinedException("ln(0)")
        elif aValue < 0:
            raise ValueUndefinedException("ln(negative)")
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
        variable: Variable
    ) -> Result:
        aValue, aPartial, aDependsOn = self.a.derive(variable).toTriple()
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
        variable: Variable
    ) -> Result:
        aValue, aPartial, aDependsOn = self.a.derive(variable).toTriple()
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
        variable: Variable
    ) -> Result:
        aValue, aPartial, aDependsOn = self.a.derive(variable).toTriple()
        bValue, bPartial, bDependsOn = self.b.derive(variable).toTriple()
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
        variable: Variable
    ) -> Result:
        aValue, aPartial, aDependsOn = self.a.derive(variable).toTriple()
        bValue, bPartial, bDependsOn = self.b.derive(variable).toTriple()
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
        variable: Variable
    ) -> Result:
        aValue, aPartial, aDependsOn = self.a.derive(variable).toTriple()
        bValue, bPartial, bDependsOn = self.b.derive(variable).toTriple()
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
        variable: Variable
    ) -> Result:
        aValue, aPartial, aDependsOn = self.a.derive(variable).toTriple()
        bValue, bPartial, bDependsOn = self.b.derive(variable).toTriple()
        if bValue == 0:
            if aValue == 0:
                raise IndeterminateFormException("0 / 0")
            else:
                raise ValueUndefinedException("non-zero / 0")
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
    # In case (I), we support negative bases. In case (II), we do not support negative bases.
    def derive(
        self: Power,
        variable: Variable
    ) -> Result:
        aValue, aPartial, aDependsOn = self.a.derive(variable).toTriple()
        bValue, bPartial, bDependsOn = self.b.derive(variable).toTriple()
        resultDependsOn = aDependsOn | bDependsOn
        # !!! consider a more flexible check for bValue being an integer
        if (variable not in bDependsOn) and bValue.is_integer(): # CASE I: has constant integral exponent
            if bValue >= 2:
                if aValue == 0:
                    resultValue = 0
                    resultPartial = bValue * (aValue ** (bValue - 1)) * aPartial
                    return Result(resultValue, resultPartial, resultDependsOn)
                else: # aValue != 0
                    resultValue = aValue ** bValue
                    resultPartial = (bValue * resultValue / aValue) * aPartial
                    return Result(resultValue, resultPartial, resultDependsOn)
            elif bValue == 1:
                resultValue = aValue
                resultPartial = aPartial
                return Result(resultValue, resultPartial, resultDependsOn)
            elif bValue == 0:
                if aValue == 0:
                    raise IndeterminateFormException("0 ** 0") # !!! think through this once more
                else: # aValue != 0
                    resultValue = 1
                    resultPartial = 0
                    return Result(resultValue, resultPartial, resultDependsOn)
            else: # bValue <= -1:
                if aValue == 0:
                    raise ValueUndefinedException("0 ** negative")
                else: # aValue != 0
                    resultValue = aValue ** bValue
                    resultPartial = (bValue * resultValue / aValue) * aPartial
                    return Result(resultValue, resultPartial, resultDependsOn)
        else: # CASE II: does not have an integral exponent
            if aValue > 0:
                resultValue = aValue ** bValue
                resultPartial = (
                    (bValue * resultValue / aValue) * aPartial +
                    math.log(aValue) * resultValue * bPartial
                )
                return Result(resultValue, resultPartial, resultDependsOn)
            elif aValue == 0:
                if bValue > 0:
                    raise IndeterminateFormException("ln(0) * 0")
                elif bValue == 0:
                    raise IndeterminateFormException("ln(0) * (0 ** 0)")
                else: # bValue < 0
                    raise ValueUndefinedException("0 ** negative")
            else: # aValue < 0:
                raise ValueUndefinedException("negative ** non-integer")

# !!!
# bValue * (aValue ** (bValue - 1)) * aPartial +
# math.log(aValue) * (aValue ** bValue) * bPartial

# !!! kill the below comments when I'm done with them

# u ** v is well defined if
# (uValue > 0) or (uValue = 0 and vValue > 0) or (uValue < 0 and v is a constant integer)

# If i'm going to evaluate u ** v and v * u ** (v - 1) * du + ln(u) * u ** v * dv
# I'll need uValue > 0 because of the log. But that alone (uValue > 0) is enough to guarantee
# u ** v is well defined.

# To get the log term to die, it suffices to have v be constant.
# Alternatively, it might be enough if u evaluates to 0.


##### CASE v is constant #####

# Then we're working with the formula,
# d(u ** v) = v * u ** (v - 1) * du

# For this to make sense we need both of the following:
# (A) (uValue > 0) or (uValue = 0 and vValue > 0) or (uValue < 0 and v is a constant integer)
# (B) (uValue > 0) or (uValue = 0 and vValue > 1) or (uValue < 0 and v is a constant integer)

# Putting these together,
# (uValue > 0) or (uValue = 0 and vValue > 1) or (uValue < 0 and v is a constant integer)


##### SUBCASE v is the constant, zero #####

# u ** 0 = 1 for all u != 0
# d(u ** 0) = d(1) = 0 * du


##### CASE u is the constant, zero #####

# 0 ** v = 0 for all v > 0.
# d(0 ** v) = d(0) = 0 * dv

# So for u = 0, vValue > 0, we have partial = 0


##### CASE u evaluates to 0 #####

# v * u ** (v - 1) * du + ln(u) * u ** v * dv

# we'll want v > 1 for the first part
# what's lim u->0 (ln(u) * u**2)?
# Use l'hopital!
# 2u / (- 1 / (ln(u) ** 2)) = - 2u * ( (ln(u)) ** 2 )
