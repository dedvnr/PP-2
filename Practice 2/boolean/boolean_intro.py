#1
print(bool("Hello")) #True
print(bool(15)) #True

"""the same as:
x = "Hello"
y = 15

print(bool(x))
print(bool(y))"""


#2 True values
bool("abc")
bool(123)
bool(["apple", "cherry", "banana"])


#3 False values
bool(False)
bool(None)
bool(0)
bool("")
bool(())
bool([])
bool({})


#4
class myclass():
  def __len__(self):
    return 0

myobj = myclass()
print(bool(myobj)) #False


#5
def myFunction() :
  return True

print(myFunction()) #True


#6
def myFunction() :
  return True

if myFunction():
  print("YES!")
else:
  print("NO!") #Output: YES!
  
  
#7
x = 200
print(isinstance(x, int)) #True