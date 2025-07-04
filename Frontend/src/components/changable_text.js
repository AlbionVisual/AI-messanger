import React, { useEffect, useRef } from "react";
import "./changable_text.css";

function ChangeableText(props) {
  const { initial_value, hangle_change, edit_content, style } = props;

  const editableDivRef = useRef(null);

  useEffect(() => {
    if (
      editableDivRef.current &&
      editableDivRef.current.textContent !== initial_value
    ) {
      editableDivRef.current.textContent = initial_value;
    }
  }, [initial_value]);

  const handleInput = (e) => {
    const newContent = e.target.textContent;
    if (hangle_change) {
      hangle_change(newContent);
    }
  };

  const handleBlur = (e) => {
    const finalContent = e.target.textContent;
    if (edit_content) {
      edit_content(finalContent);
    }
  };

  return (
    <div className="editable-field">
      <div
        ref={editableDivRef}
        className="changable-text"
        style={style}
        onInput={handleInput}
        onBlur={handleBlur}
        contentEditable="true"
      />
    </div>
  );
}

export default ChangeableText;
