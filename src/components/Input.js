import React from "react";

function Input({ value, onChange }) {
  return (
    <input
      className="w-100 rounded-3 p-2 mb-2"
      placeholder="insert tournament name..."
      type="text"
      value={value}
      onChange={onChange}
    />
  );
}

export default Input;
