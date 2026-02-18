#1: Method overriding

class Bird:
    def move(self):
        print("Bird flies")

class Penguin(Bird):
    def move(self):
        print("Penguin swims") #child class replaces a method from the parent class with its own version

b = Bird()
p = Penguin()

b.move()
p.move()
