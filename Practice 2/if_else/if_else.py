#1 Else Without Elif
a = 200
b = 33
if b > a:
  print("b is greater than a")
else:
  print("b is not greater than a") 
#Output:b is not greater than a
  
  
#2 Checking even or odd numbers
number = 7

if number % 2 == 0:
  print("The number is even")
else:
  print("The number is odd")
#Output:The number is odd


#3
username = "Emil"

if len(username) > 0:
  print(f"Welcome, {username}!")
else:
  print("Error: Username cannot be empty")
#Output:Welcome, Emil!


#4
x = 41

if x > 10:
  print("Above ten,")
  if x > 20:
    print("and also above 20!")
  else:
    print("but not above 20.")
"""Output:Above ten,
and also above 20!"""


#5
age = 25
has_license = True

if age >= 18:
  if has_license:
    print("You can drive")
  else:
    print("You need a license")
else:
  print("You are too young to drive")
#Output:You can drive