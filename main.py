import re
from contextlib import redirect_stdout


def build_regex(pattern_str, variables, allowed_symbols):
    # Создаём строку класса символов из массива allowed_symbols, экранируя специальные символы
    symbol_class = ''.join(re.escape(char) for char in allowed_symbols)

    # Экранируем управляющие символы в строке шаблона
    escaped_pattern = re.escape(pattern_str)

    for variable in variables:
        # Заменяем первое вхождение переменной на именованную группу, захватывающую символы из allowed_symbols
        group_pattern = f"(?P<{variable}>[{symbol_class}]+)"
        escaped_pattern = re.sub(rf"(?<!<)\b{re.escape(variable)}\b", group_pattern, escaped_pattern, count=1)

        # Заменяем все последующие вхождения переменной на ссылку на группу
        reference_pattern = f"(?P={variable})"
        escaped_pattern = re.sub(rf"(?<!<)\b{re.escape(variable)}\b", reference_pattern, escaped_pattern)

    return escaped_pattern

def extract_variables(regex, text, variables):
    """
    Извлекает значения переменных из строки, если они есть, иначе возвращает None.
    """
    match = re.search(regex, text)

    # Проверяем, если есть совпадение и соответствующие группы
    if match:
        # Используем groupdict(), чтобы получить все группы, соответствующие именам переменных
        extracted = {var: match.group(var) for var in variables if var in match.groupdict()}

        if extracted:  # Если переменные найдены, возвращаем их
            return extracted
        else:
            return None  # Возвращаем None, если переменных не найдено
    else:
        return None  # Если нет совпадений вообще, возвращаем None


def substitute_variables(pattern_str, variable_values):
    """
    Заменяет имена переменных в строке на их значения из словаря.
    """
    # Для каждой переменной и её значения заменяем в строке имя переменной на значение
    for var, value in variable_values.items():
        pattern_str = pattern_str.replace(var, value)

    return pattern_str

# Открываем файл на чтение
with open('input.txt', 'r') as file:
    data = file.read()

# Шаблон для поиска всех переменных с их значениями
pattern = r'(\w+)\s*=\s*{([^}]*)}'

# Используем словарь для сохранения переменных и их значений
variables = {}

# Находим все совпадения в тексте
matches = re.findall(pattern, data)

# Заполняем словарь значениями без внешних кавычек
for name, value in matches:
    variables[name] = value

# Пример вывода полученных значений
print(variables)

R = variables['R'].split(',')
A = variables['A'].split(',')
X = variables['X'].split(',')
A1 = variables['A1'].split(',')
#line = '111111111111111111111/1111='
match = re.search(r'line\s*=\s*(.+)', data)

if match:
    line = match.group(1)  # Извлекаем строку из найденного совпадения
else:
    line = ''

print('A:', A)
print('X:', X)
print('A1:', A1)
print('R:', R)

with open('output.txt', 'w', encoding='utf8') as f:
    with redirect_stdout(f):
        print(line)
        print('-' * 30)
        for i in line:
            if i not in A:
                print('Строка не принадлежит алфавиту A')
                exit(0)
        i = 0

        while i < len(R):
            if X!=['']:
                was, become = R[i].split('->')
                was_regex = build_regex(was, X, A1)

                # Проверяем, есть ли переменные в строке 'become'
                extracted_vars = extract_variables(was_regex, line, X)

                if extracted_vars:  # Если переменные есть, выполняем основную логику
                    become = substitute_variables(become, extracted_vars)
                    was = substitute_variables(was, extracted_vars)
                    if re.search(was_regex, line):
                        line = line.replace(was, become, 1)
                        print(line)
                        print(R[i])
                        print('-' * 30)
                        i = 0
                    else:
                        i += 1
                else:
                    if re.search(was, line):
                        line = re.sub(was, become, line)
                        print(line)
                        print(R[i])
                        print('-' * 30)
                        i = 0
                    else:
                        i += 1
            else:
                was, become = R[i].split('->')
                if re.search(was, line):

                    line = re.sub(was, become, line)
                    print(line)
                    print(R[i])
                    print('-' * 30)
                    i = 0
                else:
                    i+=1