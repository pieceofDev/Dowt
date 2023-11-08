with open("AI/text.txt") as file:
    list_examples = file.readlines()

for line in range(len(list_examples)):
    new_str = list_examples[line][:282].replace("Of the", "Of that") + list_examples[line][282:]
    list_examples[line] = new_str

with open("AI/text.txt", "w") as file:
    for line in list_examples:
        file.write(line)
