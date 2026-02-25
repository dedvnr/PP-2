#1
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  print(x)
"""Output: 
apple
banana
cherry
"""


#2
for x in "banana":
  print(x)
"""Output: 
b
a
n
a
n
a
"""


#3
for x in range(6): 
  print(x)
"""Output: 
0
1
2
3
4
5
"""

for x in range(2, 6): #using start parameter
  print(x)
"""Output: 
2
3
4
5
"""

for x in range(2, 30, 3): #increment specified
  print(x)
"""Output: 
2
5
8
11
14
17
20
23
26
29
"""


#4
for x in range(6):
  print(x)
else:
  print("Finally finished!")
"""Output: 
0
1
2
3
4
5
Finally finished!
"""


#5
adj = ["red", "big", "tasty"]
fruits = ["apple", "banana", "cherry"]

for x in adj:
  for y in fruits:
    print(x, y)
"""Output: 
red apple
red banana
red cherry
big apple
big banana
big cherry
tasty apple
tasty banana
tasty cherry
"""


#6
for x in [0, 1, 2]:
  pass
#Output: 

