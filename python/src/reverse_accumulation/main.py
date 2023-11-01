from src.reverse_accumulation.expression import Constant, Variable

print("Reverse Accumulation Method")

# Example: Finding the partials of z = x * (x + y) + 5 * y * y at (x, y) = (2, 3)
x = Variable()
y = Variable()
c = Constant(5)
z = x * (x + y) + c * y * y
variableValues = { x: 2, y: 3 }
print("z =", z.evaluate(variableValues))         # Output: z = 55
result = z.derive(variableValues)
print("∂z/∂x =", result.partialWithRespectTo(x)) # Output: ∂z/∂x = 7
print("∂z/∂y =", result.partialWithRespectTo(y)) # Output: ∂z/∂y = 32
