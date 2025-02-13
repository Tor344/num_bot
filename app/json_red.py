import json
import os

def load_data(file_path):
    """Загружает данные из JSON-файла."""
    try:
        with  open('app/data.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
        return None
    except json.JSONDecodeError:
        print(f"Ошибка декодирования JSON в файле {file_path}.")
        return None

def save_data(file_path, data):
    """Сохраняет данные в JSON-файл."""
    try:
        with open('app/data.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"Данные успешно сохранены в {file_path}.")
    except Exception as e:
        print(f"Ошибка при сохранении данных: {e}")

def update_text_in_json(file_path, item_id, new_text):
    """Изменяет текст в JSON-файле для элемента с указанным id."""
    # Загружаем данные
    data = load_data(file_path)
    if data is None:
        return

    # Ищем элемент по id
    for item in data:
        if item.get('id') == item_id:
            # Изменяем текст
            item['text'] = new_text
            print(f"Текст для id={item_id} изменен на: {new_text}")
            break
    else:
        print(f"1Элемент с id={item_id} не найден.")
        return

    # Сохраняем обновленные данные
    save_data(file_path, data)


def update_photo_in_json(file_path, item_id, new_photo):
    """Изменяет текст в JSON-файле для элемента с указанным id."""
    # Загружаем данные
    data = load_data(file_path)
    if data is None:
        return

    # Ищем элемент по id
    for item in data:
        if item.get('id') == item_id:
            # Изменяем текст
            item['photo_ids'] = new_photo
            print(f"Текст для id={item_id} изменен на: {new_photo}")
            break
    else:
        print(f"2Элемент с id={item_id} не найден.")
        return

    # Сохраняем обновленные данные
    save_data(file_path, data)

