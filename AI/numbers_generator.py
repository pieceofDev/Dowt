import re
import random


def extract_numbers(file_path):
    tuples = []
    with open(file_path, 'r', encoding="utf-8") as file:
        for line in file:
            numbers = re.findall(r'\b\d+\b', line)
            numbers = [int(n) for n in numbers]  # Convert strings to integers
            tuples.append(tuple(numbers))
    return list([i for i in tuples if i])


# Use the function with your file path
path = 'text.txt'
number_tuples = extract_numbers(path)

range_income = [int(i) for i in input("income_from_number-to_number (ex. 500-3000): ").split("-")]
range_expenses = [int(i) for i in input("expenses_from_number-to_number (ex. 500-3000): ").split("-")]

result = []

for i in range(1, int(input("How many examples do you need?: ")) + 1):
    example = [random.randint(range_income[0], range_income[1]), random.randint(range_expenses[0], range_expenses[1])]
    temp = example[1]
    cats = random.randint(0, temp)
    regular = random.randint(0, temp - cats)
    savings = temp - cats - regular
    example += [cats, regular, savings]
    if tuple(example) not in number_tuples:
        result.append(tuple(example))

for i in range(len(result)):
    print(*result[i], sep=",")
    if (i + 1) % 3 == 0:
        print()
