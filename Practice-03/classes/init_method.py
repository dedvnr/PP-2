#1: Using __init__ constructor

class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade

s1 = Student("Sasha", 11)
s1.name = "Aleksandr"

print(s1.name)
print(s1.grade)

del s1.grade
del s1
