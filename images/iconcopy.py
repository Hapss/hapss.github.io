import os
import shutil
import pandas as pd

def main():
    # === Настройки путей ===
    excel_path = r"F:\HGD\Partners_Story.xlsx"
    source_folder = r"F:\HGD\Wiki_Images\menusv2"
    dest_folder = r"C:\Users\justr\Новая папка\Документы\GitHub\.github.io\images\partners"

    # Проверка существования путей
    if not os.path.exists(excel_path):
        print(f"Ошибка: Файл Excel не найден: {excel_path}")
        return
    if not os.path.exists(source_folder):
        print(f"Ошибка: Исходная папка не найдена: {source_folder}")
        return

    os.makedirs(dest_folder, exist_ok=True)

    # === Чтение Excel ===
    print("Чтение файла Excel...")
    try:
        df = pd.read_excel(excel_path)
        if 'FigureID' not in df.columns:
            print("Ошибка: В таблице нет колонки 'FigureID'.")
            return
        figure_ids = df['FigureID'].dropna().astype(str).str.strip().unique()
    except Exception as e:
        print(f"Ошибка при чтении Excel: {e}")
        return

    # === Анализ папки назначения (что уже есть) ===
    existing_in_dest = set()
    if os.path.exists(dest_folder):
        for f in os.listdir(dest_folder):
            if os.path.isfile(os.path.join(dest_folder, f)):
                existing_in_dest.add(os.path.splitext(f)[0])

    # === Анализ исходной папки (что можно взять) ===
    source_files_map = {}
    for f in os.listdir(source_folder):
        full_path = os.path.join(source_folder, f)
        if os.path.isfile(full_path):
            name_no_ext = os.path.splitext(f)[0]
            source_files_map[name_no_ext] = f

    # === Основная логика поиска и копирования ===
    copied_count = 0
    already_exists_count = 0
    
    # Списки для отчета об отсутствующих файлах
    missing_underscore_5 = []
    missing_any_image = []

    print("Начинаю обработку ID...")

    for fid in figure_ids:
        target_5 = f"{fid}_5"
        
        # 1. Проверяем, есть ли уже файл _5 в папке partners
        if target_5 in existing_in_dest:
            already_exists_count += 1
            continue
        
        # Если _5 нет, фиксируем это для отчета
        missing_underscore_5.append(target_5)
        
        # 2. Проверяем наличие изображения БЕЗ суффикса (просто ID) в папке partners
        if fid not in existing_in_dest:
            missing_any_image.append(fid)
        
        # 3. Ищем альтернативы _4 или _6 в source_folder
        found = False
        for suffix in ["_4", "_6"]:
            search_name = f"{fid}{suffix}"
            
            if search_name in source_files_map:
                original_filename = source_files_map[search_name]
                src_path = os.path.join(source_folder, original_filename)
                dst_path = os.path.join(dest_folder, original_filename)
                
                try:
                    shutil.copy2(src_path, dst_path)
                    print(f"Найдена замена: {original_filename} (для отсутствующего {target_5})")
                    copied_count += 1
                    found = True
                    break 
                except Exception as e:
                    print(f"Ошибка при копировании {original_filename}: {e}")

    # === Итоги и отчет об отсутствующих ===
    print("\n" + "=" * 30)
    print(f"ОБРАБОТКА ЗАВЕРШЕНА")
    print("-" * 30)
    print(f"Уже было в папке partners (_5): {already_exists_count}")
    print(f"Скопировано альтернатив из menusv2 (_4 или _6): {copied_count}")
    
    if missing_underscore_5:
        print(f"\nСПИСОК ОТСУТСТВУЮЩИХ ФАЙЛОВ С '_5' В ПАПКЕ PARTNERS:")
        for item in missing_underscore_5:
            print(f" - {item}")
            
    if missing_any_image:
        print(f"\nСПИСОК ID, ДЛЯ КОТОРЫХ ВООБЩЕ НЕТ ИЗОБРАЖЕНИЙ (НИ '_5', НИ ЧИСТОГО ID):")
        for item in missing_any_image:
            print(f" - {item}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nКритическая ошибка: {e}")
    finally:
        input("\nНажмите Enter для выхода...")