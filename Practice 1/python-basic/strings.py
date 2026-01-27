#1
print("His name is'Freddy'")
print('His name is "Freddy"')
b = """To be, or not to be, that is the question (Hamlet),
All the world's a stage (As You Like It),
Some are born great, some achieve greatness, and some have greatness thrust upon them (Twelfth Night)."""
print(b)
print(b[1])
print(len(b))
for x in "Mama":
    print(x)
if "like" in b:
  print("Yes, I 'like' it.")
print("love" not in b)

#2
a = "I wanna be your vacuum cleaner"
print(a[2:7])
print(a[:7])
print(a[11:])
print(a[-7:-2])
print(a.upper())
print(a.lower())
print(a.replace("e", "a"))
print(a.split(" "))

#3
a = "Hello"
b = "World"
c = a + " " + b
print(c)

#4
price = 59
txt = f"The price is {price:.2f} dollars"
print(txt)
txt1 = f"The price is {20 * 59} dollars"
print(txt1)

#5
txt2 = "We are the so-called \"Vikings\" from the north."