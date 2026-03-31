import os
import shutil

def organize_partner_images():
    # Путь к исходной папке (откуда берем)
    src_root = r"F:\HGD\DecryptedAssets\v3\assets\assetbundles\menusv2\map\figure\partner"
    
    # Путь к целевой папке (куда кладем)
    dst_dir = r"C:\Users\justr\Новая папка\Документы\GitHub\.github.io\images\partners"

    # Создаем целевую папку, если она не существует
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
        print(f"Создана целевая папка: {dst_dir}")

    count = 0
    ignored_count = 0

    print("Начинаю поиск и копирование файлов...")

    # os.walk позволяет заходить во все подпапки рекурсивно
    for root, dirs, files in os.walk(src_root):
        for filename in files:
            # Проверяем расширения (обычно png или jpg)
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                
                # Условие: исключаем файлы с припиской (1) в названии
                if "(1)" in filename:
                    ignored_count += 1
                    continue
                
                # Полный путь к исходному файлу
                src_path = os.path.join(root, filename)
                # Полный путь к месту назначения
                dst_path = os.path.join(dst_dir, filename)

                try:
                    # Используем copy2 для сохранения метаданных (даты изменения и т.д.)
                    shutil.copy2(src_path, dst_path)
                    count += 1
                    # Раскомментируйте строку ниже, если хотите видеть каждый файл в консоли:
                    # print(f"Скопирован: {filename}")
                except Exception as e:
                    print(f"Ошибка при копировании {filename}: {e}")

    print("-" * 30)
    print(f"Завершено!")
    print(f"Всего скопировано файлов: {count}")
    print(f"Пропущено копий с '(1)': {ignored_count}")

if __name__ == "__main__":
    organize_partner_images()