#1: Function with return value

def add(a, b):
    """Returns sum."""
    return a + b

result = add(5, 7)
print("Sum:", result)


#2: Multiple return values

def min_max(numbers):
    return min(numbers), max(numbers)

mn, mx = min_max([4, 8, 1, 9])
print("Min:", mn, "Max:", mx)
