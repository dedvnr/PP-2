#1: Class variable vs instance variable

class Employee:
    company = "Apple"  # class variable - belongs to the class itself

    def __init__(self, name):
        self.name = name  # instance variable - belongs to each object

e1 = Employee("A")
e2 = Employee("B")

print(e1.company) #since company is not inside e1 or e2 → Python checks class → finds it
print(e2.company) #Output:"Apple"

# Change class variable
Employee.company = "Pear"

print(e1.company)
print(e2.company)
