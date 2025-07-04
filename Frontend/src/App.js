import React, { useState, useEffect } from "react";
import Chat from "./components/chat.js";
import Selector from "./components/selector.js";
import "./App.css";

function App() {
  const [chat_id, set_chat_id] = useState([]);

  const chat_change = (new_chat_id) => {
    set_chat_id(new_chat_id);
  };

  return (
    <div className="App">
      <Selector onChatChange={chat_change}></Selector>
      <Chat chat_id={chat_id}></Chat>
    </div>
  );
}

export default App;
