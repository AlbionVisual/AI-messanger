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

def dialog_list_request(dict_return : bool = False) -> list:
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
            id = cursor.lastrowid
            conn.commit()
            cursor.close()
            return id
        finally:
            if conn:
                conn.close()
    else:
        raise TypeError("Name cannot be non string or None")
    
def remove_dialog(dialog_id : int):
    """
    @brief Удаляет чаты с указанным id
    @param id ключ удалямых чатов
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
    
def edit_dialog_name(dialog_id : int, new_dialog_name : str):
    """
    @brief Изменяет имя на новое для чата с указанным идентификатором
    @param dialog_id ключ чата, для изменения имени
    @param new_dialog_name новое имя для чата
    """
    if isinstance(dialog_id, int) and isinstance(new_dialog_name, str) and new_dialog_name:
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE conversations SET title = %s WHERE id = %s", (new_dialog_name, dialog_id))
            conn.commit()
            cursor.close()
        finally:
            if conn:
                conn.close()
    else:
        raise TypeError("Id or new name cannot be wrong types nor None")

def message_list_request(conversation_id : int, dict_return : bool = False) -> list:
    """
    @brief Получить список всех сообщений по id чата
    @param conversation_id id диалога из которого нужно получить сообщения
    @param dict_return возвращать в виде словарей или кортежей
    @returns список сообщений из чата
    """

    if isinstance(conversation_id,int):
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=dict_return)
            cursor.execute("SELECT * FROM messages WHERE conversation_id = %s", (conversation_id,))
            ans = cursor.fetchall()
            return ans
        finally:
            if conn:
                conn.close()
    else: 
        raise TypeError("coversation_id should be integer")
    
def message_insert(conversation_id : int, is_user : bool, text : str ):
    """
    @brief Вставить сообщение в чат по id чата
    @param conversation_id идентификатор диалога в который нужно вставить сообщения
    @param is_user если true то сообщение пользователя, если false то сообщение от ai
    @param text текст сообщения 
    """

    if isinstance(conversation_id,int) and isinstance(is_user,bool) and isinstance(text,str):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO messages (conversation_id, sender, content) VALUES (%s,%s,%s)", (conversation_id, 'user' if is_user else 'ai', text))
            id = cursor.lastrowid
            conn.commit()
            cursor.close()
            return id
        except mysql.connector.Error as err:
            print("we have an error inserting to database" + str(err))
            conn.rollback()
        finally:
            if conn:
                conn.close()
    
    else: 
        raise TypeError("Params types is not match")
    

def message_delete(id : int):
    """
    @brief Удалить сообщение по id в чате с conversation_id
    @param id идентификатор сообщения   
    """

    if isinstance(id, int):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM messages WHERE id =  %s", (id,))
            conn.commit()

        except mysql.connector.Error as err:
            print("we have an error inserting to database" + str(err))
            conn.rollback()
        finally:
            if conn:
                conn.close()
    
    else: 
        raise TypeError("id should be integer")

def edit_message_request(message_id : int, new_message : str):
    """
    @brief Изменяет имя на новое для чата с указанным идентификатором
    @param message_id ключ чата, для изменения имени
    @param new_message новый текст сообщения
    """
    # UPDATE conversations SET title = 'Третий диалог' WHERE id = 22
    if isinstance(message_id, int) and isinstance(new_message, str) and new_message:
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE messages SET content = %s WHERE id = %s", (new_message, message_id))
            conn.commit()
            cursor.close()
        finally:
            if conn:
                conn.close()
    else:
        raise TypeError("Id or new name cannot be other types nor None")

if __name__ == "__main__":
    edit_message_request(6, "Третий диалог")
    print(message_list_request(22))
    #print(dialog_list_request(dict_return=True))
    # lst = [(el['id'], el['title']) for el in dialog_list_request(dict_return=True)]
    # print("Before modifying:\n" + '\n'.join([el[1] for el in lst]))
    # print("Adding nth dialog...")
    # add_new_dialog("nth dialog")
    # lst = [(el['id'], el['title']) for el in dialog_list_request(dict_return=True)]
    # print("After first modifying:\n" + '\n'.join([el[1] for el in lst]))
    # print("Removing last...")
    # remove_dialog(int(lst[-1][0]))
    # lst = [(el['id'], el['title']) for el in dialog_list_request(dict_return=True)]
    # print("After second modifying:\n" + '\n'.join([el[1] for el in lst]))
