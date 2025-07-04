import React, { useState, useEffect } from "react";
import ChangeableText from "./changable_text";
import "./chat.css";

function Chat(props) {
  const [messages, set_messages] = useState([]);
  const [message_text, set_message_text] = useState("");

  useEffect(() => {
    show_messages(props.chat_id);
  }, [props]);

  const show_messages = async (chat_id) => {
    try {
      if (!chat_id) throw new Error("Нету ChatId");
      const response = await fetch(
        `http://127.0.0.1:5000/api/messages/${chat_id}`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      if (!response.ok) {
        throw new Error("Ошибка при загрузке сообщений");
      }
      const result = await response.json();
      set_messages(result);
    } catch (error) {
      console.error("Ошибка:", error);
    }
  };

  const add_message = async (is_user) => {
    try {
      const new_message = {
        chat_id: props.chat_id,
        content: message_text,
        sender: is_user,
      };

      const response = await fetch("http://127.0.0.1:5000/api/messages", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(new_message),
      });

      if (!response.ok) {
        throw new Error("Ошибка при добавлении сообщения");
      }

      const result = await response.json();
      set_messages((prev_messages) => [...prev_messages, result.message]);

      if (is_user) {
        set_message_text("");
        await add_message(false);
      }
    } catch (error) {
      console.error("Ошибка:", error);
    }
  };

  const delete_message = async (id) => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/api/messages/${id}`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
      });
      if (!response.ok) {
        throw new Error("Ошибка при удалении сообщения");
      }
      set_messages(messages.filter((message) => message.id !== id));
    } catch (error) {
      console.error("Ошибка:", error);
    }
  };

  const edit_message = async (id, value) => {
    const new_message = {
      content: value,
    };
    const response = await fetch(`http://127.0.0.1:5000/api/messages/${id}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(new_message),
    });

    if (!response.ok) {
      throw new Error("Ошибка при изменении сообщения");
    } else {
      set_messages(
        messages.map((message) => {
          if (message.id == id) {
            return {
              id: message.id,
              content: value,
              sender: message.sender,
            };
          } else return message;
        })
      );
    }
  };

  return (
    <div className="chat">
      {props.chat_id && (
        <div className="chat-section">
          <h2>Сообщения</h2>
          <div className="message-input">
            <input
              type="text"
              value={message_text}
              onChange={(e) => set_message_text(e.target.value)}
              placeholder="Напишите сообщение..."
            />
            <button
              onClick={() => {
                add_message(true);
              }}>
              Отправить
            </button>
          </div>

          <ul className="message-list">
            {messages.map((message) => (
              <li key={message.id} className="message">
                <ChangeableText
                  style={{ float: message.sender ? "right" : "left" }}
                  className="message-text"
                  end_change={(new_value) =>
                    edit_message(message.id, new_value)
                  }
                  initial_value={message.content}></ChangeableText>
                <button
                  onClick={() => delete_message(message.id)}
                  className="delete-button">
                  Удалить
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default Chat;
