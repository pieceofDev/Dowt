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
    matching_lines = {tuple(lines): numbers for numbers, lines in numbers_dict.items() if len(lines) > 1}
    return matching_lines


file_path = 'text.txt'
with open(file_path, 'r', encoding='utf-8') as file:
    file_content = file.read()

# Остальная часть кода...


# Использование функции с содержимым файла
matching_lines = find_matching_lines(file_content)
print(matching_lines)

# Example text content
example_text = """Hi. I'm glad you reached out to me for advice. According to last month, your income was $0 dollars and your expenses were $15300 dollars. Of that $7650 dollars you spent on miscellaneous categories, $6650 dollars in recurring payments, and $1000 dollars in savings, I think:
Hi. I'm glad you reached out to me for advice. According to last month, your income was $0 dollars and your expenses were $15300 dollars. Of that $7650 dollars you spent on miscellaneous categories, $6650 dollars in recurring payments, and $1000 dollars in savings, I think:"""

# Find matching lines
# find_matching_lines(example_text)
