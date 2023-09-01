import React from "react";
import trash from "../assets/img/trash.svg";

function InputPlayerDelete({ input, playerName, onRemove, onChange }) {
  return (
    <div className="player_input d-flex justify-content-between align-center mb-1">
      <div className="input_counter_container me-4">
        <img src={input} alt={input} />
      </div>
      <input
        className="w-100 rounded-3 p-2 mb-2 me-2"
        placeholder="insert player name here..."
        type="text"
        value={playerName}
        onChange={onChange}
      />
      <button className="secondary_button_small" onClick={onRemove}>
        <img src={trash} alt={trash} />
      </button>
    </div>
  );
}

export default InputPlayerDelete;
