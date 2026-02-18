#1: *args — variable number of positional arguments

def total_sum(*numbers):
    """Returns sum of all arguments"""
    return sum(numbers)

print(total_sum(1, 2, 3, 4))


#2: **kwargs — variable number of named arguments

def print_info(**data):
    """Prints key-value pairs"""
    for key, value in data.items():
        print(key, "=", value)

print_info(name="Azhar", age=16, city="Almaty") #packed into a dictionary automatically
