import React, { useState } from "react";
import "./changable_text.css";

function ChangeableText(props) {
  const [field_value, set_field_value] = useState(props.value);

  const edit_content = (new_content) => {
    if (props.end_change) props.end_change(new_content);
  };
  const hangle_change = (new_content) => {
    if (props.handle_change) props.handle_change(new_content);
  };

  return (
    <div className="editable-field">
      <input
        className="changable-text"
        type="text"
        value={field_value}
        style={props.style}
        onChange={(e) => {
          hangle_change(e.target.value);
          set_field_value(e.target.value);
        }}
        onBlur={(e) => edit_content(e.target.value)}
      />
    </div>
  );
}

export default ChangeableText;
