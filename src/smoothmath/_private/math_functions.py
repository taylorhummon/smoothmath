from __future__ import annotations
from typing import TYPE_CHECKING
import math
import smoothmath._private.errors as er
import smoothmath._private.utilities as util
if TYPE_CHECKING:
    from smoothmath import RealNumber


def add(
    *args: RealNumber
) -> RealNumber:
    return sum(args)


def minus(
    x: RealNumber,
    y: RealNumber
) -> RealNumber:
    return x - y


def negation(
    x: RealNumber
) -> RealNumber:
    return - x


def multiply(
    *args: RealNumber
) -> RealNumber:
    product = 1
    for arg in args:
        if arg == 0:
            return 0
        product *= arg
    return product


def divide(
    x: RealNumber,
    y: RealNumber
) -> RealNumber:
    if y == 0:
        if x == 0:
            raise er.DomainError("divide(x, y) is not smooth around (x = 0, y = 0)")
        else: # x != 0
            raise er.DomainError("divide(x, y) blows up around x != 0 and y = 0")
    else:
        return x / y


def reciprocal(
    x: RealNumber
) -> RealNumber:
    if x == 0:
        raise er.DomainError("reciprocal(x) blows up around x = 0")
    else:
        return 1 / x


def power(
    x: RealNumber,
    y: RealNumber
) -> RealNumber:
    if x == 0:
        if y > 0:
            raise er.DomainError("power(x, y) is not smooth around x = 0 for y > 0")
        elif y == 0:
            raise er.DomainError("power(x, y) is not smooth around (x = 0, y = 0)")
        else: # y < 0
            raise er.DomainError("power(x, y) blows up around x = 0 for y < 0")
    elif x < 0:
        raise er.DomainError("power(x, y) is undefined for x < 0")
    else: # x > 0
        return x ** y


def nth_power(
    x: RealNumber,
    n: int
) -> RealNumber:
    if n <= 0:
        raise er.DomainError(f"nth_power(x, n) is not defined for n = {n}")
    else:
        return x ** n


def nth_root(
    x: RealNumber,
    n: int
) -> RealNumber:
    if n <= 0:
        raise er.DomainError(f"nth_root(x, n) is not defined for n = {n}")
    elif n == 1:
        return x
    elif n == 2:
        if x > 0:
            return math.sqrt(x)
        elif x == 0:
            raise er.DomainError(f"nth_root(x, n) is not defined at x = 0 for n = 2")
        else: # x < 0
            raise er.DomainError(f"nth_root(x, n) is not defined for negative x for n = 2")
    elif n == 3:
        if x > 0:
            return math.cbrt(x)
        elif x == 0:
            raise er.DomainError(f"nth_root(x, n) is not defined at x = 0 for n = 3")
        else: # x < 0
            # CAREFUL: math.cbrt can return imaginary values for negative inputs
            return - math.cbrt(- x)
    else: # n >= 4
        if util.is_even(n):
            if x > 0:
                return x ** (1 / n)
            elif x == 0:
                raise er.DomainError(f"nth_root(x, n) is not defined at x = 0 for n = {n}")
            else: # x < 0
                raise er.DomainError(f"nth_root(x, n) is not defined for negative x for n = {n}")
        else: # n is odd
            if x > 0:
                return x ** (1 / n)
            elif x == 0:
                raise er.DomainError(f"nth_root(x, n) is not defined at x = 0 for n = {n}")
            else: # x < 0
                return - ((- x) ** (1 / n))


def exponential(
    x: RealNumber,
    base: RealNumber = math.e
) -> RealNumber:
    if base <= 0:
        raise er.DomainError(f"exponential(x) must have a positive base, found: {base}")
    else:
        return base ** x


def logarithm(
    x: RealNumber,
    base: RealNumber = math.e
) -> RealNumber:
    if base <= 0:
        raise er.DomainError("logarithm(x) must have a positive base")
    elif base == 1:
        raise er.DomainError("logarithm(x) cannot have base = 1")
    return math.log(x, base)


def cosine(
    x: RealNumber
) -> RealNumber:
    return math.cos(x)


def sine(
    x: RealNumber
) -> RealNumber:
    return math.sin(x)
