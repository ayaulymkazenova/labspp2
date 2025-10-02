import math

class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    def show(self):
        print(f"({self.x}, {self.y})")
    
    def move(self, x, y):
        self.x = x
        self.y = y
    
    def dist(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

#Example
x1 = float(input("Enter x for point 1: "))
y1 = float(input("Enter y for point 1: "))
x2 = float(input("Enter x for point 2: "))
y2 = float(input("Enter y for point 2: "))

p1 = Point(x1, y1)
p2 = Point(x2, y2)

p1.show()
p2.show()
print("Distance:", p1.dist(p2))