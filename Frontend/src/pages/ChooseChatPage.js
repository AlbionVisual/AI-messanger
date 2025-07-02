import React, { useState } from "react";

function ChooseChatPage(props) {
  const [chosenChat, setChosenChat] = useState(null);
  const [chatList, setChatList] = useState([1, 2, 4]);

  return (
    <div className="chat-list">
      {chatList.map((key) => {
        return (
          <div key={key}>
            {key == chosenChat ? (
              <h1>Элемент списка: {key}</h1>
            ) : (
              <h3>Элемент списка: {key}</h3>
            )}
            <button onClick={() => setChosenChat(key)}>Сделать активным</button>
            <br></br>
          </div>
        );
      })}
    </div>
  );
}

export default ChooseChatPage;
