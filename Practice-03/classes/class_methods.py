#1: Instance methods and self

class Rectangle:
    def __init__(self, w, h):
        self.width = w
        self.height = h

    def area(self):
        return self.width * self.height

r = Rectangle(4, 5)
print("Area:", r.area())
