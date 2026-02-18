#1: Using lambda with map() for transformation

numbers = [1, 2, 3, 4]

# Square each number
squared = list(map(lambda x: x**2, numbers))

print(squared) #[1, 4, 9, 16]
