#1: Using lambda with filter() for selection

numbers = [5, 12, 7, 18, 3]

# Keep only numbers > 10
filtered = list(filter(lambda x: x > 10, numbers))

print(filtered) #[12, 18]

