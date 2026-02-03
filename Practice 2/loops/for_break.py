#1
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  print(x)
  if x == "banana":
    break
"""Output: 
apple
banana
"""

fruits = ["apple", "banana", "cherry"]
for x in fruits:
  if x == "banana":
    break
  print(x)
"""Output: 
apple
"""


#2
for x in range(6):
  if x == 3: break
  print(x)
else:
  print("Finally finished!")
"""Output: 
0
1
2
"""
  