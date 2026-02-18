#1: Positional argument

def power(base, exponent):
    print(base ** exponent)

power(2, 3)


#2 Default argument

def country(name="Kazakhstan"):
    print("Country:", name)

country()
country("Japan")


#3 Passing list as argument

def print_list(items):
    for item in items:
        print(item)

print_list([1, 2, 3, 4])
