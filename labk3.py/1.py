class MyClass:
    def __init__(self):
        self.string = ""
    
    def getString(self):
        self.string = input()
    
    def printString(self):
        print(self.string.upper())

# Example
obj = MyClass()
obj.getString()
obj.printString() 