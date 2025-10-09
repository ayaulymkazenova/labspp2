class Shape:
    def area(self):
        return 0


class Rectangle(Shape):
    def __init__(self, length, width):
        self.length = length
        self.width = width
    
    def area(self):
        return self.length * self.width


# Example
if __name__ == "__main__":
    shape = Shape()
    print(f"Shape area: {shape.area()}")  
    
    rectangle = Rectangle(5, 3)
    print(f"Rectangle area: {rectangle.area()}")  