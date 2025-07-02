from dotenv import load_dotenv
import os
import mysql.connector

def get_connection():
    """
    @brief Открывает соединение с базой даннхы по начальным данным из .env и возвращает его
    @returns mysql.connector.Connect()
    """
    load_dotenv()

    db_user = os.getenv("MYSQL_USER")
    db_host = os.getenv('MYSQL_HOST')
    db_password = os.getenv("MYSQL_PASSWORD")
    db_name = os.getenv('MYSQL_DB')

    return mysql.connector.connect(host=db_host, user=db_user, password=db_password, database=db_name)

def dialog_list_request(dict_return : bool = False):
    """
    @brief Получает и возвращает список всех доступных чатов
    @param dict_return Возвращать ли значение в виде словаря (в противном случае будет кортеж)
    @returns отдаёт список словарей или кортежей с информацией о чатах
    """
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=dict_return)
        cursor.execute("SELECT * FROM conversations")
        ans = cursor.fetchall()
        cursor.close()
        return ans
    finally:
        if conn:
            conn.close()

def add_new_dialog(dialog_name : str):
    """
    @brief добавляет строку в базу данных с чатами
    @param dialog_name название вставляемого чата
    """
    if isinstance(dialog_name, str):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO conversations (title) VALUES (%s)", (dialog_name,))
            conn.commit()
            cursor.close()
        finally:
            if conn:
                conn.close()
    else:
        raise TypeError("Name cannot be non string or None")
    
def remove_dialog(dialog_id : int):
    """
    @brief Удаляет чаты с указанным id
    @param id - ключ удалямых чатов
    """
    if isinstance(dialog_id, int):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM conversations WHERE id = %s", (dialog_id,))
            conn.commit()
            cursor.close()
        finally:
            if conn:
                conn.close()
    else:
        raise TypeError("Id cannot be non integer or None")


if __name__ == "__main__":
    lst = [(el['id'], el['title']) for el in dialog_list_request(dict_return=True)]
    print("Before modifying:\n" + '\n'.join([el[1] for el in lst]))
    print("Adding nth dialog...")
    add_new_dialog("nth dialog")
    lst = [(el['id'], el['title']) for el in dialog_list_request(dict_return=True)]
    print("After first modifying:\n" + '\n'.join([el[1] for el in lst]))
    print("Removing last...")
    remove_dialog(int(lst[-1][0]))
    lst = [(el['id'], el['title']) for el in dialog_list_request(dict_return=True)]
    print("After second modifying:\n" + '\n'.join([el[1] for el in lst]))