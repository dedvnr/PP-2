#1: Parent and child class

class Animal: #parent
    def speak(self):
        print("Animal makes a sound")

class Dog(Animal): #child
    pass #a child class automatically gets the methods and properties of a parent class

d = Dog()
d.speak()
