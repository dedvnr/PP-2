#1: Using super()

class Person:
    def __init__(self, name):
        self.name = name

class Student(Person):
    def __init__(self, name, grade):
        super().__init__(name) #inherited method name from parent class
        self.grade = grade

s = Student("Serezha", 12)

print(s.name, s.grade)
