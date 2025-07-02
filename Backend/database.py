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


def message_list_request(conversation_id : int ):

    """
    @brief  Получить список всех сообщения по id чата
    @param conn конектор между pythob и mysql
    @param conversation_id id диалога из которого нужно получить сообщения
    @returns список сообщений из чата
    """

    if isinstance(conversation_id,int):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM messages WHERE conversation_id = %s", (conversation_id,))
            ans = cursor.fetchall()
            return ans
        finally:
            if conn:
                conn.close()
    else: 
        raise TypeError("coversation_id should be integer")
    
       
def message_insert(*,conversation_id : int, is_user : bool, text : str ):

    """
    @brief Вставить сообщение в чат по id чата
    @param conversation_id id диалога в который нужно вставить сообщения
    @param is_user если true то сообщение пользователя, если false то сообщение от ai
    @param text текст сообщения 
    """

    if isinstance(conversation_id,int) and isinstance(is_user,bool) and isinstance(text,str):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO messages (conversation_id, sender, content) VALUES (%s,%s,%s)", (conversation_id, 'user' if is_user else 'ai', text))
            conn.commit()
        except mysql.connector.Error as err:
            print("we have an error inserting to database" + str(err))
            conn.rollback()
        finally:
            if conn:
                conn.close()
    
    else: 
        raise TypeError("Params types is not match")
    

def message_delete(*,id : int):

    """
    @brief Удалить сообщение по id в чате с conversation_id
    @param id id - сообщения
    @param conversation_id id диалога в который нужно вставить сообщения
    
    
    """

    if isinstance(id,int):
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



if __name__ == "__main__":
    
    #message_insert(conversation_id = 1,is_user = True,text = 'ggggg')
    print(message_list_request(1))
    message_delete(id = 6)
    print(message_list_request(1))