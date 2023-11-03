from __future__ import annotations
import math
from src.dual_number.custom_types import Real
from src.dual_number.custom_exceptions import DomainException

# !!! add comments that give the differential rules

# A dual number takes the form
#    realPart + infinitesimalPart * ε
# where ε ≠ 0 and ε² = 0

class DualNumber:
    @classmethod
    def epsilon(
        cls # !!! what's the type annotation?
    ) -> DualNumber:
        return DualNumber(0, 1) # !!! use cls

    @classmethod
    def fromReal(
        cls, # !!! what's the type annotation?
        real: Real
    ) -> DualNumber:
        return DualNumber(real, 0) # !!! use cls

    def __init__(
        self: DualNumber,
        realPart: Real,
        infinitesimalPart: Real
    ) -> None:
        self.realPart = realPart
        self.infinitesimalPart = infinitesimalPart

    def __eq__(
        self: DualNumber,
        other: DualNumber
    ) -> bool:
        return (
            self.realPart == other.realPart and
            self.infinitesimalPart == other.infinitesimalPart
        )

    def __str__(
        self: DualNumber
    ) -> str:
        if self.infinitesimalPart >= 0:
            return f"{self.realPart} + {self.infinitesimalPart} * ε"
        else: # self.infinitesimalPart < 0
            return f"{self.realPart} - {- self.infinitesimalPart} * ε"

    def toPair(
        self: DualNumber
    ) -> tuple[Real, Real]:
        return (self.realPart, self.infinitesimalPart)

    ### Unary Operators ###

    def __neg__(
        self: DualNumber
    ) -> DualNumber:
        return DualNumber(
            - self.realPart,
            - self.infinitesimalPart
        )

    ### Binary Operators ###

    def __add__(
        self: DualNumber,
        other: DualNumber
    ) -> DualNumber:
        return DualNumber(
            self.realPart + other.realPart,
            self.infinitesimalPart + other.infinitesimalPart
        )

    def __sub__(
        self: DualNumber,
        other: DualNumber
    ) -> DualNumber:
        return DualNumber(
            self.realPart - other.realPart,
            self.infinitesimalPart - other.infinitesimalPart
        )

    def __mul__(
        self: DualNumber,
        other: DualNumber
    ) -> DualNumber:
        return DualNumber(
            self.realPart * other.realPart,
            other.realPart * self.infinitesimalPart + self.realPart * other.infinitesimalPart
        )

    def __truediv__(
        self: DualNumber,
        other: DualNumber
    ) -> DualNumber:
        if other.realPart == 0:
            if self.realPart == 0:
                raise DomainException("(a1 + b1 * ε) / (a2 + b2 * ε) for a1 = 0 and a2 = 0")
            else:
                raise DomainException("(a1 + b1 * ε) / (a2 + b2 * ε) for a1 != 0 and a2 = 0")
        return DualNumber(
            self.realPart / other.realPart,
            (
                other.realPart * self.infinitesimalPart - self.realPart * other.infinitesimalPart
            ) / (
                other.realPart ** 2
            )
        )

    def __pow__(
        self: DualNumber,
        other: DualNumber
    ) -> DualNumber:
        raise Exception("Operator ** is not supported on dual numbers. Consider using power1D() or power2D() instead.")

### Functions that work on dual numbers

def reciprocal(
    u: DualNumber
) -> DualNumber:
    uRealPart, uInfinitesimalPart = u.toPair()
    if uRealPart == 0:
        raise DomainException("reciprocal(a + b * ε) for a = 0")
    return DualNumber(
        1 / uRealPart,
        - uInfinitesimalPart / uRealPart ** 2
    )

def squareRoot(
    u: DualNumber
) -> DualNumber:
    uRealPart, uInfinitesimalPart = u.toPair()
    if uRealPart == 0:
        raise DomainException("squareRoot(a + b * ε) for a = 0")
    if uRealPart < 0:
        raise DomainException("squareRoot(a + b * ε) for a < 0")
    resultRealPart = math.sqrt(uRealPart)
    return DualNumber(
        resultRealPart,
        uInfinitesimalPart / (2 * resultRealPart)
    )

def naturalExponential(
    u: DualNumber
) -> DualNumber:
    uRealPart, uInfinitesimalPart = u.toPair()
    resultRealPart = math.e ** uRealPart
    return DualNumber(
        resultRealPart,
        resultRealPart * uInfinitesimalPart
    )

def naturalLogarithm(
    u: DualNumber
) -> DualNumber:
    uRealPart, uInfinitesimalPart = u.toPair()
    if uRealPart == 0:
        raise DomainException("naturalLogarithm(a + b * ε) for a = 0")
    if uRealPart < 0:
        raise DomainException("naturalLogarithm(a + b * ε) for a < 0")
    return DualNumber(
        math.log(uRealPart),
        uInfinitesimalPart / uRealPart
    )

def sine(
    u: DualNumber
) -> DualNumber:
    uRealPart, uInfinitesimalPart = u.toPair()
    return DualNumber(
        math.log(uRealPart),
        uInfinitesimalPart / uRealPart
    )

def cosine(
    u: DualNumber
) -> DualNumber:
    uRealPart, uInfinitesimalPart = u.toPair()
    return DualNumber(
        math.log(uRealPart),
        uInfinitesimalPart / uRealPart
    )

def power1D(
    base: DualNumber,
    exponent: int
) -> DualNumber:
    if not exponent.is_integer():
        raise Exception("must provide an integer as the second argument to power1D()")
    baseRealPart, baseInfinitesimalPart = base.toPair()
    if exponent >= 2:
        return DualNumber(
            baseRealPart ** exponent,
            exponent * (baseRealPart ** (exponent - 1)) * baseInfinitesimalPart
        )
    elif exponent == 1:
        return DualNumber(baseRealPart, baseInfinitesimalPart)
    elif exponent == 0:
        return DualNumber(1, 0)
    else: # exponent <= -1
        if baseRealPart == 0:
            raise DomainException("power1D(a + b * ε, k) for a = 0 and k negative integer")
        return DualNumber(
            baseRealPart ** exponent,
            exponent * (baseRealPart ** (exponent - 1)) * baseInfinitesimalPart
        )

def power2D(
    base: DualNumber,
    exponent: DualNumber
) -> DualNumber:
    baseRealPart, baseInfinitesimalPart = base.toPair()
    exponentRealPart, exponentInfinitesimalPart = exponent.toPair()
    if baseRealPart > 0:
        resultRealPart = baseRealPart ** exponentRealPart
        return DualNumber(
            resultRealPart,
            exponentRealPart * (resultRealPart / baseRealPart) * baseInfinitesimalPart +
            math.log(baseRealPart) * resultRealPart * exponentInfinitesimalPart
        )
    elif baseRealPart == 0:
        raise DomainException("power2D(a1 + b1 * ε, a2 + b2 * ε) for a1 = 0.")
    else: # baseRealPart < 0
        raise DomainException("power2D(a1 + b1 * ε, a2 + b2 * ε) for a1 < 0.")

### Taking Derivatives ###

def derive(
    f, # !!! function type
    x: Real
) -> Real:
    return f(DualNumber(x, 1)).infinitesimalPart

def partial1(
    f, # !!! function type
    x: Real,
    y: Real
) -> Real:
    return f(DualNumber(x, 1), DualNumber.fromReal(y)).infinitesimalPart

def partial2(
    f, # !!! function type
    x: Real,
    y: Real
) -> Real:
    return f(DualNumber.fromReal(x), DualNumber(y, 1)).infinitesimalPart

def directionalDerivative(
    f, # !!! function type
    x: Real,
    y: Real,
    v1: Real,
    v2: Real
) -> Real:
    coefficient = 1 / math.sqrt(v1 ** 2 + v2 ** 2)
    return f(
        DualNumber(x, coefficient * v1),
        DualNumber(y, coefficient * v2)
    ).infinitesimalPart
