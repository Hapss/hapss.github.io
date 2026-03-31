import re
import os

def remove_story_from_js(content):
    """
    Удаляет параметр 'story' и его объектное содержимое из JavaScript кода.
    Работает с форматами 'story: { ... }' или '"story": { ... }'.
    """
    # Регулярное выражение для поиска начала ключа story
    # Ищет 'story:', '"story":' или "'story':" с последующей открывающей скобкой {
    pattern = re.compile(r'([\'"]?story[\'"]?\s*:\s*\{)')
    
    while True:
        match = pattern.search(content)
        if not match:
            break
            
        start_index = match.start()
        brace_start = match.end() - 1
        
        # Счётчик фигурных скобок для корректного поиска конца объекта story
        bracket_count = 0
        end_index = -1
        
        for i in range(brace_start, len(content)):
            if content[i] == '{':
                bracket_count += 1
            elif content[i] == '}':
                bracket_count -= 1
                
            if bracket_count == 0:
                end_index = i + 1
                break
        
        if end_index != -1:
            # Удаляем найденный блок и возможную запятую после него
            tail = content[end_index:]
            comma_match = re.match(r'^\s*,', tail)
            if comma_match:
                end_index += comma_match.end()
            
            content = content[:start_index] + content[end_index:]
        else:
            # Если не нашли закрывающую скобку (ошибка структуры), прерываемся
            break
            
    return content

def main():
    # Настройки имен файлов
    input_file = 'partners.js'   # Ваш исходный файл на 22к строк
    output_file = 'result.js' # Файл, который получится на выходе
    
    if not os.path.exists(input_file):
        print(f"Файл {input_file} не найден! Переименуйте ваш файл в {input_file}")
        return

    print("Чтение файла...")
    with open(input_file, 'r', encoding='utf-8') as f:
        js_code = f.read()

    print(f"Обработка {len(js_code)} символов...")
    cleaned_code = remove_story_from_js(js_code)

    print("Сохранение результата...")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(cleaned_code)
    
    print(f"Готово! Результат в файле: {output_file}")

if __name__ == "__main__":
    main()