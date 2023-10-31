from src.reverse_accumulation.expression import Constant, Variable

print("Reverse Accumulation Method")

# Example: Finding the partials of z = x * (x + y) + 5 * y * y at (x, y) = (2, 3)
x = Variable(2)
y = Variable(3)
c = Constant(5)
z = x * (x + y) + c * y * y
print("z =", z.evaluate())                                 # Output: z = 55
result = z.derive()
print("∂z/∂x =", result.partialWithRespectTo(x)) # Output: ∂z/∂x = 7
print("∂z/∂y =", result.partialWithRespectTo(y)) # Output: ∂z/∂y = 32