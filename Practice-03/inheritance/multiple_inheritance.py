#1: Multiple inheritance

class Flyer:
    def fly(self):
        print("Flying")

class Swimmer:
    def swim(self):
        print("Swimming")

class Duck(Flyer, Swimmer):
    pass #inherits all methods from both base classes

d = Duck()
d.fly()
d.swim()
