#1
a = 200
b = 33
if b > a:
  print("b is greater than a")
elif a == b:
  print("a and b are equal")
else:
  print("a is greater than b")
#Output:a is greater than b


#2
temperature = 22

if temperature > 30:
  print("It's hot outside!")
elif temperature > 20:
  print("It's warm outside")
elif temperature > 10:
  print("It's cool outside")
else:
  print("It's cold outside!")
#Output:It's warm outside


#3
value = 50

if value < 0:
  print("Negative value")
elif value == 0:
  pass # Zero case - no action needed
else:
  print("Positive value")
#Output:Positive value

#4
score = 92
extra_credit = 5

if score >= 90:
  if extra_credit > 0:
    print("A+ grade")
  else:
    print("A grade")
elif score >= 80:
  print("B grade")
else:
  print("C grade or below")
#Output:A+ grade