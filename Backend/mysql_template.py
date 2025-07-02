from dotenv import load_dotenv
import os
import mysql.connector

load_dotenv() # Загружает переменные из .env файла

db_user = os.getenv("MYSQL_USER")
db_host = os.getenv('MYSQL_HOST')
db_password = os.getenv("MYSQL_PASSWORD")
db_name = os.getenv('MYSQL_DB')
openai_api_key = os.getenv('OPENAI_API_KEY')

conn = mysql.connector.connect(host=db_host, user=db_user, password=db_password, database=db_name)

cursor = conn.cursor()

cursor.execute("SELECT * FROM conversations WHERE title = %s", ('Первый диалог',))
print(cursor.fetchall())

try:
    cursor.execute("INSERT INTO conversations (title) VALUES (%s)", ('Третий диалог',))
    conn.commit()
except mysql.connector.Error as err:
    print("we have an error inserting to database" + err)
    conn.rollback()

cursor.execute("SELECT * FROM conversations")
print(cursor.fetchall())

cursor.close()