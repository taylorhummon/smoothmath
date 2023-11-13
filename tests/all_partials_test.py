from smoothmath.all_partials import AllPartials
from smoothmath.expressions.variable import Variable

def testAllPartials():
    w = Variable("w")
    x = Variable("x")
    y = Variable("y")
    all_partials = AllPartials()
    all_partials._add_seed(x, 3)
    all_partials._add_seed(y, 4)
    all_partials._add_seed(y, 2)
    assert all_partials.partial_with_respect_to(w) == 0
    assert all_partials.partial_with_respect_to(x) == 3
    assert all_partials.partial_with_respect_to(y) == 6
    assert all_partials.partial_with_respect_to("y") == 6
