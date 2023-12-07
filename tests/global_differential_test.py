from pytest import approx, raises
from smoothmath import Point, DomainError, GlobalPartial, LocalDifferential
from smoothmath.expression import Variable, Constant, Reciprocal, Square, Logarithm
from smoothmath._private.global_differential import GlobalDifferentialBuilder


def test_GlobalDifferential():
    w = Variable("w")
    x = Variable("x")
    y = Variable("y")
    original_expression = Constant(4) * w + x * y ** Constant(3)
    synthetic_w_partial = Constant(4)
    synthetic_x_partial = y ** Constant(3)
    synthetic_y_partial = Constant(3) * x * Square(y)
    builder = GlobalDifferentialBuilder(original_expression)
    builder.add_to(w, synthetic_w_partial)
    builder.add_to(x, synthetic_x_partial)
    builder.add_to(y, synthetic_y_partial)
    global_differential = builder.build()
    point = Point({w: 7, x: 4, y: 5})
    # component_at() method
    assert global_differential.component_at(point, w) == approx(4)
    assert global_differential.component_at(point, x) == approx(125)
    assert global_differential.component_at(point, y) == approx(300)
    # component() method
    global_w_partial = global_differential.component(w)
    global_x_partial = global_differential.component(x)
    global_y_partial = global_differential.component(y)
    assert global_differential.component(w).at(point) == approx(4)
    assert global_differential.component(x).at(point) == approx(125)
    assert global_differential.component(y).at(point) == approx(300)
    assert global_w_partial.original_expression == original_expression
    assert global_x_partial.original_expression == original_expression
    assert global_y_partial.original_expression == original_expression
    assert global_w_partial == GlobalPartial(original_expression, synthetic_w_partial)
    assert global_x_partial == GlobalPartial(original_expression, synthetic_x_partial)
    assert global_y_partial == GlobalPartial(original_expression, synthetic_y_partial)
    # at() method
    local_differential = global_differential.at(point)
    assert local_differential.component(w) == approx(4)
    assert local_differential.component(x) == approx(125)
    assert local_differential.component(y) == approx(300)
    assert local_differential.original_expression == original_expression
    desired = LocalDifferential(original_expression, point, {"w": 4, "x": 125, "y": 300})
    assert local_differential == desired


def test_GlobalDifferential_raises():
    x = Variable("x")
    original_expression = Logarithm(x)
    synthetic_x_partial = Reciprocal(x)
    builder = GlobalDifferentialBuilder(original_expression)
    builder.add_to(x, synthetic_x_partial)
    global_differential = builder.build()
    point = Point({x: -1})
    with raises(DomainError):
        global_differential.component_at(point, x)
    global_x_partial = global_differential.component(x)
    with raises(DomainError):
        global_x_partial.at(point)
    with raises(DomainError):
        global_differential.at(point)


def test_LocalDifferential_equality():
    x = Variable("x")
    y = Variable("y")
    builder_a = GlobalDifferentialBuilder(Constant(23))
    builder_a.add_to(x, Constant(3))
    builder_a.add_to(y, Constant(4))
    global_differential_a = builder_a.build()
    builder_b = GlobalDifferentialBuilder(Constant(23))
    builder_b.add_to(y, Constant(4))
    builder_b.add_to(x, Constant(3))
    global_differential_b = builder_b.build()
    assert global_differential_a == global_differential_b
    builder_c = GlobalDifferentialBuilder(Constant(23))
    builder_c.add_to(x, Constant(4))
    builder_c.add_to(y, Constant(3))
    global_differential_c = builder_c.build()
    assert global_differential_a != global_differential_c


def test_LocalDifferential_hashing():
    x = Variable("x")
    y = Variable("y")
    builder_a = GlobalDifferentialBuilder(Constant(23))
    builder_a.add_to(x, Constant(3))
    builder_a.add_to(y, Constant(4))
    global_differential_a = builder_a.build()
    builder_b = GlobalDifferentialBuilder(Constant(23))
    builder_b.add_to(y, Constant(4))
    builder_b.add_to(x, Constant(3))
    global_differential_b = builder_b.build()
    assert hash(global_differential_a) == hash(global_differential_b)
