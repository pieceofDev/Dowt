def replace_saving_with_goals(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    updated_lines = []
    for line in lines:
        # Разделяем строку на две части: до и после "I think:"
        parts = line.split("I think:")
        # Заменяем "saving" на "goals" только в первой части
        parts[0] = parts[0].replace("they returned", "you spent")
        # Объединяем части обратно
        updated_line = "I think:".join(parts)
        updated_lines.append(updated_line)

    # Перезаписываем файл с обновленными строками
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(updated_lines)

# Вызываем функцию для файла 'text.txt'
replace_saving_with_goals('text.txt')
