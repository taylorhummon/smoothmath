Usage
=====

Derivatives
-----------

>>> from smoothmath.expression import Variable, Constant
>>> x = Variable("x")
>>> z = x ** Constant(2) + Constant(3)
>>> z.evaluate(1)
4
>>> z.derivative(5)
10


Partials
--------

>>> from smoothmath import Point
>>> from smoothmath.expression import Variable, Constant
>>> x = Variable("x")
>>> z = x ** 2 + Constant(3)
>>> z.evaluate(Point(x=1))
4
>>> z.local_partial(x, Point(x=1))
2


>>> from smoothmath import Point, GlobalPartial
>>> from smoothmath.expression import Variable, Constant
>>> x = Variable("x")
>>> z = x ** 2 + Constant(3)
>>> global_partial = GlobalPartial(z, x)
>>> global_partial.at(Point(x=1))
2
>>> global_partial.at(Point(x=2))
4
>>> global_partial.as_expression()
Multiply(Constant(2), Variable("x"))


Differentials
-------------
