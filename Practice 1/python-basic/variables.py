#1
x = 5
y = "Azhar"
print(x)
print(y)

#2
x = 4       # x is of type int
x = "Nargiz" # x is now of type str
print(x)

#3
x = str(4)    # x will be '4'
y = int(4)    # y will be 4
z = float(4)  # z will be 4.0

#4
x = 5
y = "John"
print(type(x))
print(type(y))

#5
a = 4
A = "Sally"
#A will not overwrite a

#6
x = "awesome"

def myfunc():
  x = "fantastic"
  print("Python is " + x)

myfunc()

print("Python is " + x)