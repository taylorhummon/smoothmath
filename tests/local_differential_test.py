from smoothmath import Point
from smoothmath.expression import Variable, Constant
from smoothmath._private.local_partials_accumulator import LocalPartialsAccumulator

# # !!!
# def test_LocalDifferential():
#     w = Variable("w")
#     x = Variable("x")
#     y = Variable("y")
#     builder = LocalPartialsAccumulator(Constant(23), Point(w = 7, x = 8, y = 9))
#     builder.add_to(x, 3)
#     builder.add_to(y, 4)
#     builder.add_to(y, 2)
#     local_differential = builder.build()
#     assert local_differential.component(w) == 0
#     assert local_differential.component(x) == 3
#     assert local_differential.component(y) == 6
#     assert local_differential.component("w") == 0
#     assert local_differential.component("x") == 3
#     assert local_differential.component("y") == 6


# def test_LocalDifferential_equality():
#     x = Variable("x")
#     y = Variable("y")
#     builder_a = LocalPartialsAccumulator(Constant(23), Point(x = 8, y = 9))
#     builder_a.add_to(x, 3)
#     builder_a.add_to(y, 4)
#     local_differential_a = builder_a.build()
#     builder_b = LocalPartialsAccumulator(Constant(23), Point(y = 9, x = 8))
#     builder_b.add_to(y, 4)
#     builder_b.add_to(x, 3)
#     local_differential_b = builder_b.build()
#     assert local_differential_a == local_differential_b
#     builder_c = LocalPartialsAccumulator(Constant(23), Point(x = 8, y = 9))
#     builder_c.add_to(x, 4)
#     builder_c.add_to(y, 3)
#     local_differential_c = builder_c.build()
#     assert local_differential_a != local_differential_c


# def test_LocalDifferential_hashing():
#     x = Variable("x")
#     y = Variable("y")
#     builder_a = LocalPartialsAccumulator(Constant(23), Point(x = 8, y = 9))
#     builder_a.add_to(x, 3)
#     builder_a.add_to(y, 4)
#     local_differential_a = builder_a.build()
#     builder_b = LocalPartialsAccumulator(Constant(23), Point(y = 9, x = 8))
#     builder_b.add_to(y, 4)
#     builder_b.add_to(x, 3)
#     local_differential_b = builder_b.build()
#     assert hash(local_differential_a) == hash(local_differential_b)
