import React from "react";

function InputPlayer({ input, playerName, onChange }) {
  return (
    <div className="player_input d-flex justify-content-between align-center mb-1">
      <div className="input_user_container me-4">
        <img className="h-100" src={input} alt={input} />
      </div>
      <input
        className="w-100 rounded-3 p-2 mb-2"
        placeholder="insert player name here..."
        type="text"
        value={playerName}
        onChange={onChange}
      />
    </div>
  );
}

export default InputPlayer;
