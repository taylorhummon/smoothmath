from expression import Constant, Variable

# Example: Finding the partials of z = x * (x + y) + 5 * y * y at (x, y) = (2, 3)
x = Variable(2)
y = Variable(3)
c = Constant(5)
z = x * (x + y) + c * y * y
xPartial = z.evaluateAndDerive(x).partial
yPartial = z.evaluateAndDerive(y).partial
print("∂z/∂x =", xPartial) # Output: ∂z/∂x = 7
print("∂z/∂y =", yPartial) # Output: ∂z/∂y = 32
