import React, { useState, useEffect } from 'react';
import "./App.css";


function App() {
  const [chats, set_chats] = useState([]);
  const [chat_name, set_chat_name] = useState('');

  const [messages, set_messages] = useState([]);
  const [message_text, set_message_text] = useState('');
  const [select_chat_id, set_select_chat_id] = useState(null);

  useEffect(() => {
      // Запрос к Flask API с использованием fetch
      fetch('http://127.0.0.1:5000/api/chats')
        .then(response => {
          if (!response.ok) {
            throw new Error('Ошибка при загрузке данных');
          }
          return response.json();
        })
        .then(data => set_chats(data))
        .catch(error => console.error('Ошибка:', error));
    }, []);

  const add_chat = async () => {
    const new_chat = { chat_name };  // id генерируется на сервере

    try {
      const response = await fetch('http://127.0.0.1:5000/api/chats', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(new_chat),
      });
      if (!response.ok) {
        throw new Error('Ошибка при добавлении чата');
      }
      const result = await response.json();
      set_chats([...chats, result.chat]); // Добавляем новый чат из ответа сервера
      set_chat_name(''); // Очищаем поле ввода
    } catch (error) {
        console.error('Ошибка:', error);
      }
  };


const delete_chat = async (id) => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/api/chats/${id}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      if (!response.ok) {
        throw new Error('Ошибка при удалении чата');
      }
      set_chats(chats.filter(chat => chat.id !== id)); // Удаляем чат из состояния
    } catch (error) {
      console.error('Ошибка:', error);
    }
  };

  const show_messages = async (chat_id) => {
    set_select_chat_id(chat_id);

    try {
      const response = await fetch(`http://127.0.0.1:5000/api/messages/${chat_id}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      if (!response.ok) {
        throw new Error('Ошибка при загрузке сообщений');
      }
      const result = await response.json();
      set_messages(result);
    } catch (error) {
      console.error('Ошибка:', error);
    }
  };
  
const add_message = async (is_user) => {
    
    const new_message = { chat_id: select_chat_id, text: message_text, sender: is_user };

    try {
      const response = await fetch('http://127.0.0.1:5000/api/messages', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(new_message),
      });

      if (!response.ok) {
        throw new Error('Ошибка при добавлении сообщения');
      }

      const result = await response.json();
      set_messages((prev_messages) => [...prev_messages, result.message]);

      if (is_user) {
        set_message_text('');
        await add_message(false);
      }

    } catch (error) {
      console.error('Ошибка:', error);
    }
  };

  const delete_message = async (id) => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/api/messages/${id}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      if (!response.ok) {
        throw new Error('Ошибка при удалении сообщения');
      }
      set_messages(messages.filter(message => message.id !== id)); 
    } catch (error) {
      console.error('Ошибка:', error);
    }
  };

  return (
    <div className="App">
      

      <ul className="chats">
        <h2>Чаты</h2>
          {chats.map(chats => (
            <li key={chats.id}
            className={`chat-item ${select_chat_id === chats.id ? 'selected' : ''}`}
            onClick={() => show_messages(chats.id)}
            >
              <button onClick={() => show_messages(chats.id)} >Выбрать</button>
              <span  className="chat-name"> {chats.title}</span>
              
              <button onClick={() => delete_chat(chats.id)} className="delete-button">Удалить</button>
            </li>
          ))}
        </ul>

        <div className="chat-input">
          <input
            type="text"
            value={chat_name}
            onChange={(e) => set_chat_name(e.target.value)}
            placeholder="Напишите название чата..."
          />
          <button onClick={add_chat}>Добавить</button>
        </div>

        {select_chat_id && (
        <div className="messages-section">
          <h2>Сообщения</h2>
          <div className="message-input">
            <input
              type="text"
              value={message_text}
              onChange={(e) => set_message_text(e.target.value)}
              placeholder="Напишите сообщение..."
            />
            <button onClick={() => {add_message(true)}}>Отправить</button>
            

          </div>
          <ul className="chat-messages">
            {messages.map(message => (
              <li key={message.id} className="chat-message">
                <span style={{float: message.is_user? 'right' : 'left'}} className="message-text">{message.content}</span>
                <button onClick={() => delete_message(message.id)} className="delete-button">Удалить</button>
                
              </li>
            ))}
          </ul>
        </div>
      )}

    </div>
  );
}

export default App;
