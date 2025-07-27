# AI Messenger

Web-приложение помогающее общаться с современными LLM через бесплатное API от Openrouter. Демонстрирует работу с базами данных, а также связи бэкенд-фронтенд.

Проект делался в качестве проекта летней практики в 2025-ом году. Требованиями было только наличие: python-бэкенда, web-приложения, сайта-презентации (или презентация проекта напрямую показав его), подключённой базы данных (4 запроса: добавить, получить, обновить, удалить) - всё это работает.

## Для запуска

Необходимо наличие MySQL (server + shell), Git и NodeJS на компьютере. Всё это можно скачать с официальных сайтов. Для запуска проекта выполните команды в свободной папке:

### 1. Склонируйте репозиторий

```bash
git clone https://github.com/AlbionVisual/AI-messanger.git
```

### 2. Создайте локальную базу данных

В любом интерфейсе с доступом к MySQL выполнить:

```sql
CREATE DATABASE ai_chat_db;
USE ai_chat_db;
CREATE TABLE conversations (
    id INT AUTO_INCREMENT PRIMARY KEY, -- Целое число, автоинкремент, первичный ключ
    title VARCHAR(255) NOT NULL DEFAULT 'Новый диалог', -- Текст до 255 символов, не может быть пустым, значение по умолчанию
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Дата/время создания, по умолчанию текущее время
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP -- Дата/время обновления, обновляется при изменении строки
);
CREATE TABLE messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    conversation_id INT NOT NULL, -- Внешний ключ, ссылается на conversations.id
    sender ENUM('user', 'ai') NOT NULL, -- Перечисление, может быть 'user' или 'ai'
    content TEXT NOT NULL, -- Длинный текст
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE -- При удалении диалога, удаляются и все связанные сообщения
);
```

Подробнее о командах MySQL можно почитать в документации.

### 3. Запустите отдельно бэкенд и фронтенд

**Внутри папки `Backend` склонированного проекта:**

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

**Внутри `Frontend`:**

```powershell
npm install
npm run start
```

Получить доступ можно в браузере. По умолчанию на localhost:3000

## Технологии

- React
- Python 3
  - Flask
- MySQL

## Интерфейс

**Пользователь может:**

- Создавать новый чат
- Писать туда сообщения и получать ответ от заданной в коде нейронной сети
- Редактировать название чата, а также содержание любых сообщений
- Удалять сообщения

Все сообщения хранятся в базе данных.

![Интерфейс чата программы](https://github.com/AlbionVisual/AI-messanger/blob/main/clips/Chat-demonstation.png)

Также сообщения автоматически подгружаются при открытии приложения, либо нового чата.

![Интерфейс работы с чатами](https://github.com/AlbionVisual/AI-messanger/blob/main/clips/Chat-selection.png)
