#1 One-line if statement
a = 5
b = 2
if a > b: print("a is greater than b")
#Output:a is greater than b


#2 One-line if/else that prints a value
a = 2
b = 330
print("A") if a > b else print("B") 
#Output:B


#3 Assign a Value With If ... Else
a = 10
b = 20
bigger = a if a > b else b
print("Bigger is", bigger)
#Output:Bigger is 20


#4 Multiple Conditions on One Line
a = 330
b = 330
print("A") if a > b else print("=") if a == b else print("B")
#Output:=


#5 Finding the maximum of two numbers
x = 15
y = 20
max_value = x if x > y else y
print("Maximum value:", max_value)
#Output:Maximum value: 20


#6
username = ""
display_name = username if username else "Guest"
print("Welcome,", display_name)
#Output:Welcome, Guest