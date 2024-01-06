import re
from collections import defaultdict


def find_matching_lines(file_content):
    # Dictionary to store the lines with their corresponding sets of numbers
    numbers_dict = defaultdict(list)

    # Splitting the file content into lines
    lines = file_content.split('\n')

    # Regular expression to find numbers following the dollar sign
    regex = r'\$\d+'

    # Process each line, skipping even-numbered lines
    for line_number, line in enumerate(lines, 1):
        # Skip even-numbered lines
        if line_number % 2 == 0:
            continue

        # Find all numbers in the current line
        numbers = re.findall(regex, line)
        # Sort and convert numbers to a tuple for easy comparison
        numbers_tuple = tuple(sorted(numbers))
        # Add line number to the dictionary
        numbers_dict[numbers_tuple].append(line_number)

    # Finding and returning lines with matching number sets
    return numbers_dict


file_path = 'text.txt'
with open(file_path, 'r', encoding='utf-8') as file:
    file_content = file.read()

# Остальная часть кода...


# Использование функции с содержимым файла
matching_lines = find_matching_lines(file_content)
print(matching_lines)
