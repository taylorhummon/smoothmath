from expression import Constant, Variable

# Example: Finding the partials of z = x * (x + y) + 5 *  y * y at (x, y) = (2, 3)
x = Variable(2)
y = Variable(3)
c = Constant(5)
z = x * (x + y) + c * y * y
computedPartials = z.derive()
print("z =", z.value)                                      # Output: z = 55
print("∂z/∂x =", computedPartials.partialWithRespectTo(x)) # Output: ∂z/∂x = 7
print("∂z/∂y =", computedPartials.partialWithRespectTo(y)) # Output: ∂z/∂y = 32
