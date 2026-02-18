#1: Simple function and its calling

def greet(name):
    """Prints a greeting message"""
    print("Hello,", name)

greet("Azhar") #calling and passing arguments
greet("Student")


#2: Function without parameters

def say_hello():
    """Prints a fixed message"""
    print("Hello World")

say_hello() 


#3 Reusable code

def fahrenheit_to_celsius(fahrenheit):
  return (fahrenheit - 32) * 5 / 9

print(fahrenheit_to_celsius(77))
print(fahrenheit_to_celsius(95))
print(fahrenheit_to_celsius(50))
