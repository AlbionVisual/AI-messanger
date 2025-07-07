import React, { use, useEffect, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";
import "./changable_text.css";

function ChangeableText(props) {
  const { initial_value, hangle_change, edit_content, style } = props;

  const editableDivRef = useRef(null);
  const [is_markdown_view, set_is_markdown_view] = useState(true);
  const [message, set_message] = useState(initial_value);

  useEffect(() => {
    if (
      editableDivRef.current &&
      editableDivRef.current.textContent !== initial_value
    ) {
      editableDivRef.current.textContent = initial_value;
    }
  }, [initial_value]);
  useEffect(() => {
    if (editableDivRef.current) {
      editableDivRef.current.textContent = message;
      editableDivRef.current.focus();
    }
  }, [is_markdown_view]);

  const handleInput = (e) => {
    const newContent = e.target.textContent;
    if (hangle_change) {
      hangle_change(newContent);
    }
  };

  const handleBlur = (e) => {
    const finalContent = e.target.textContent;
    if (finalContent) {
      if (edit_content) {
        edit_content(finalContent);
      }
      set_message(finalContent);
    }
    set_is_markdown_view(true);
  };

  const handleMardownClick = (e) => {
    set_is_markdown_view(false);
    console.log(e);
  };

  return (
    <>
      {is_markdown_view ? (
        <div className="markdown-field" onClick={handleMardownClick}>
          <ReactMarkdown children={message} />
        </div>
      ) : (
        <div className="editable-field">
          <div
            className="changable-text"
            ref={editableDivRef}
            style={style}
            onInput={handleInput}
            onBlur={handleBlur}
            contentEditable="true"></div>
        </div>
      )}
    </>
  );
}

export default ChangeableText;
