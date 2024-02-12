from pytest import approx
from smoothmath import Point
from smoothmath.expression import Variable, Constant, Add, Minus, Negation, Multiply, Logarithm


def test_2_ary_Add():
    x = Variable("x")
    y = Variable("y")
    z = Add(x, y)
    point = Point(x = 2, y = 3)
    assert z.evaluate(point) == approx(5)
    assert z.local_partial(point, x) == approx(1)
    assert z.local_partial(point, y) == approx(1)
    assert z.global_partial(x).at(point) == approx(1)
    assert z.global_partial(y).at(point) == approx(1)
    local_differential = z.local_differential(point)
    assert local_differential.component(x) == approx(1)
    assert local_differential.component(y) == approx(1)
    global_differential = z.global_differential()
    assert global_differential.component_at(point, x) == approx(1)
    assert global_differential.component_at(point, y) == approx(1)


def test_2_ary_Add_composition():
    x = Variable("x")
    y = Variable("y")
    z = Add(Constant(5) * x, Constant(4) * y)
    point = Point(x = 2, y = 3)
    assert z.evaluate(point) == approx(22)
    assert z.local_partial(point, x) == approx(5)
    assert z.local_partial(point, y) == approx(4)
    assert z.global_partial(x).at(point) == approx(5)
    assert z.global_partial(y).at(point) == approx(4)
    local_differential = z.local_differential(point)
    assert local_differential.component(x) == approx(5)
    assert local_differential.component(y) == approx(4)
    global_differential = z.global_differential()
    assert global_differential.component_at(point, x) == approx(5)
    assert global_differential.component_at(point, y) == approx(4)


def test_3_ary_Add():
    w = Variable("w")
    x = Variable("x")
    y = Variable("y")
    z = Add(w, x, y)
    point = Point(w = 1, x = 2, y = 3)
    assert z.evaluate(point) == approx(6)
    assert z.local_partial(point, w) == approx(1)
    assert z.local_partial(point, x) == approx(1)
    assert z.local_partial(point, y) == approx(1)
    assert z.global_partial(w).at(point) == approx(1)
    assert z.global_partial(x).at(point) == approx(1)
    assert z.global_partial(y).at(point) == approx(1)
    local_differential = z.local_differential(point)
    assert local_differential.component(w) == approx(1)
    assert local_differential.component(x) == approx(1)
    assert local_differential.component(y) == approx(1)
    global_differential = z.global_differential()
    assert global_differential.component_at(point, w) == approx(1)
    assert global_differential.component_at(point, x) == approx(1)
    assert global_differential.component_at(point, y) == approx(1)


def test_3_ary_Add_composition():
    w = Variable("w")
    x = Variable("x")
    y = Variable("y")
    z = Add(Constant(6) * w, Constant(5) * x, Constant(4) * y)
    point = Point(w = 1, x = 2, y = 3)
    assert z.evaluate(point) == approx(28)
    assert z.local_partial(point, w) == approx(6)
    assert z.local_partial(point, x) == approx(5)
    assert z.local_partial(point, y) == approx(4)
    assert z.global_partial(w).at(point) == approx(6)
    assert z.global_partial(x).at(point) == approx(5)
    assert z.global_partial(y).at(point) == approx(4)
    local_differential = z.local_differential(point)
    assert local_differential.component(w) == approx(6)
    assert local_differential.component(x) == approx(5)
    assert local_differential.component(y) == approx(4)
    global_differential = z.global_differential()
    assert global_differential.component_at(point, w) == approx(6)
    assert global_differential.component_at(point, x) == approx(5)
    assert global_differential.component_at(point, y) == approx(4)


def test_1_ary_Add():
    x = Variable("x")
    z = Add(x)
    point = Point(x = 2)
    assert z.evaluate(point) == approx(2)
    assert z.local_partial(point, x) == approx(1)
    assert z.global_partial(x).at(point) == approx(1)
    local_differential = z.local_differential(point)
    assert local_differential.component(x) == approx(1)
    global_differential = z.global_differential()
    assert global_differential.component_at(point, x) == approx(1)


def test_1_ary_Add_composition():
    x = Variable("x")
    z = Add(Constant(5) * x)
    point = Point(x = 2)
    assert z.evaluate(point) == approx(10)
    assert z.local_partial(point, x) == approx(5)
    assert z.global_partial(x).at(point) == approx(5)
    local_differential = z.local_differential(point)
    assert local_differential.component(x) == approx(5)
    global_differential = z.global_differential()
    assert global_differential.component_at(point, x) == approx(5)


def test_0_ary_Add():
    z = Add()
    point = Point()
    assert z.evaluate(point) == approx(0)


def test_Add_normalization():
    v = Variable("v")
    w = Variable("w")
    x = Variable("x")
    y = Variable("y")
    # flattening
    z = Add(Add(v), Add(Add(w, x), y), Add())
    assert z._normalize() == Add(v, w, x, y)
    # with Constant
    z = Add(Constant(2), x, Constant(3))
    assert z._normalize() == Add(x, Constant(5))
    z = Add(x, Constant(0))
    assert z._normalize() == x
    z = Add(Constant(0), x)
    assert z._normalize() == x
    z = Add(Constant(-1), x, Constant(1))
    assert z._normalize() == x
    # with Negation
    z = Add(x, y)
    assert z._normalize() == Add(x, y)
    z = Add(x, Negation(y))
    assert z._normalize() == Minus(x, y)
    z = Add(Negation(x), y)
    assert z._normalize() == Minus(y, x)
    z = Add(Negation(x), Negation(y))
    assert z._normalize() == Negation(Add(x, y))
    z = Add(Negation(w), x, Negation(y))
    assert z._normalize() == Minus(x, Add(w, y))
    z = Add(w, Negation(x), y)
    assert z._normalize() == Minus(Add(w, y), x)
    z = Add(Negation(v), w, Negation(x), y)
    assert z._normalize() == Minus(Add(w, y), Add(v, x))
    # with Logarithms
    z = Add(Logarithm(x, base = 2), Logarithm(y, base = 2))
    assert z._normalize() == Logarithm(Multiply(x, y), base = 2)
    z = Add(Logarithm(x, base = 2), Logarithm(y, base = 3))
    assert z._normalize() == Add(Logarithm(x, base = 2), Logarithm(y, base = 3))
    z = Add(Logarithm(v, base = 2), Logarithm(w, base = 3), Logarithm(x, base = 2), y)
    assert z._normalize() == Add(y, Logarithm(Multiply(v, x), base = 2), Logarithm(w, base = 3))
