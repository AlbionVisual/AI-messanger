import React, { useState, useEffect } from "react";
import ChangeableText from "./changable_text";
import "./selector.css";

function Selector(props) {
  const [chats, set_chats] = useState([]);
  const [chat_name, set_chat_name] = useState("");
  const [selected_chat_id, set_selected_chat_id] = useState(null);

  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/chats")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Ошибка при загрузке данных");
        }
        return response.json();
      })
      .then((data) => {
        set_chats(data);
        data && data[0] && data[0].id && change_selected_chat_id(data[0].id);
      })
      .catch((error) => console.error("Ошибка:", error));
  }, []);

  const change_selected_chat_id = (new_id) => {
    props.onChatChange && props.onChatChange(new_id);
    props.onChatChange && set_selected_chat_id(new_id);
  };

  const toggleSidebar = () => {
      setIsSidebarOpen(!isSidebarOpen);
  };
      
  const add_chat = async () => {
    const new_chat = { chat_name };

    try {
      const response = await fetch("http://127.0.0.1:5000/api/chats", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(new_chat),
      });
      if (!response.ok) {
        throw new Error("Ошибка при добавлении чата");
      }
      const result = await response.json();
      set_chats([...chats, result.chat]);
      set_chat_name("");
    } catch (error) {
      console.error("Ошибка:", error);
    }
  };

  const delete_chat = async (id) => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/api/chats/${id}`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
      });
      if (!response.ok) {
        throw new Error("Ошибка при удалении чата");
      }
      set_chats(chats.filter((chat) => chat.id !== id)); // Удаляем чат из состояния
    } catch (error) {
      console.error("Ошибка:", error);
    }
  };

  const handle_end_change = async (id, new_name) => {
    const request = {
      content: new_name,
    };
    const response = await fetch(`http://127.0.0.1:5000/api/chats/${id}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error("Ошибка при изменении имени чата");
    } else {
      set_chats(
        chats.map((chat) => {
          if (chat.id === id) {
            chat.title = new_name;
          }
          return chat;
        })
      );
    }
  };

  return (
    <div className="chat-selector">
      
     <button
        className="menu-toggle"
        onClick={toggleSidebar}
      >
        ☰ 
      </button>
      <div className={`sidebar ${isSidebarOpen ? "open" : "hidden"}`}>
        <div className="sidebar-header">
          <div className="chat-list">
          <h2>Чаты</h2>
          {chats.map((chats) => (
            <div
              key={chats.id}
              className={`chat-item-list ${
                selected_chat_id === chats.id ? "selected-chat" : ""
              }`}
              onClick={() => change_selected_chat_id(chats.id)}>
              <div className="chat-item">
              
                <ChangeableText
                  className="chat-name"
                  initial_value={chats.title}
                  end_change={(new_val) => {
                    handle_end_change(chats.id, new_val);
                  }}></ChangeableText>

                <button
                  onClick={() => delete_chat(chats.id)}
                  className="chat-delete-button">
                  Удалить
                </button>
              </div>
          </div>
        ))}
      <div className="chat-input">
        <input
          type="text"
          value={chat_name}
          onChange={(e) => set_chat_name(e.target.value)}
          placeholder="Напишите название чата..."
          onKeyPress={(e) => {
            if (e.key === "Enter") {
              e.preventDefault();
              add_chat(e);
            }
          }}
        />
        
      </div>
      <button className="input-button" onClick={add_chat}>Добавить</button>
      </div>
        </div>
        
    </div>
      
    </div>
  );
}

export default Selector;
