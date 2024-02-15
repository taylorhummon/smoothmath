Usage
=====

Derivatives
-----------

>>> from smoothmath.expression import Variable, Constant
>>> x = Variable("x")
>>> z = x ** Constant(2) + Constant(3)
>>> z.evaluate(1)
4
>>> z.derivative_at(5)
10


Partials
--------

>>> from smoothmath import Point
>>> from smoothmath.expression import Variable, Constant
>>> x = Variable("x")
>>> z = x ** 2 + Constant(3)
>>> z.evaluate(Point(x=1))
4
>>> z.partial_at(x, Point(x=1))
2


>>> from smoothmath import Point, Partial
>>> from smoothmath.expression import Variable, Constant
>>> x = Variable("x")
>>> z = x ** 2 + Constant(3)
>>> partial = Partial(z, x)
>>> partial.at(Point(x=1))
2
>>> partial.at(Point(x=2))
4
>>> partial.as_expression()
Multiply(Constant(2), Variable("x"))


Differentials
-------------
