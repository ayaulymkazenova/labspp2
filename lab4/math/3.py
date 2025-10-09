# 3. Area of a regular polygon
import math
n = int(input())
s = float(input())
area = (n * s ** 2) / (4 * math.tan(math.pi / n))
print(f"The area of the polygon is: {area:.0f}")