#1: Using lambda with sorted() for custom sorting

students = [
    ("Misha", 85),
    ("Danya", 92),
    ("Omar", 78)
]

# Sort by score
sorted_students = sorted(students, key=lambda s: s[1])

print(sorted_students) #[('Omar', 78), ('Azhar', 85), ('Dana', 92)]
