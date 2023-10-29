from src.forward_accumulation.expression import Constant, Variable

print("Forward Accumulation Method")

# Example: Finding the partials of z = x * (x + y) + 5 * y * y at (x, y) = (2, 3)
x = Variable()
y = Variable()
c = Constant(5)
z = x * (x + y) + c * y * y
variableValues = { x: 2, y: 3 }
xPartial = z.derive(variableValues, x).partial
yPartial = z.derive(variableValues, y).partial
print("∂z/∂x =", xPartial) # Output: ∂z/∂x = 7
print("∂z/∂y =", yPartial) # Output: ∂z/∂y = 32
