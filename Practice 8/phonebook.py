from connect import get_connection
import psycopg2

def add_user(first, last, phone):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL upsert_contact(%s::text, %s::text, %s::text)", (first, last, phone))
    conn.commit()
    print(f"Обработано: {first} {last}")
    cur.close()
    conn.close()

def find_user(name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM get_contacts_by_pattern(%s::text)", (name,))
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()
    conn.close()

def delete_user(target):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL delete_contact(%s::text)", (target,))
    conn.commit()
    print(f"Удалено: {target}")
    cur.close()
    conn.close()

def bulk_insert(first_names, last_names, phones):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL bulk_insert_contacts(%s, %s, %s)", (first_names, last_names, phones))
    conn.commit()
    print("Массовая вставка завершена")
    cur.close()
    conn.close()

if __name__ == "__main__":
    # Тестируем всё сразу:
    print("--- Добавление ---")
    add_user("Ivan", "Ivanov", "7778889900")
    
    print("--- Поиск ---")
    find_user("Ivan")
    
    print("--- Массовая вставка ---")
    bulk_insert(["Anya", "Oleg"], ["Sidorova", "Petrov"], ["7071112233", "7014445566"])
    
    print("--- Удаление ---")
    delete_user("Oleg")