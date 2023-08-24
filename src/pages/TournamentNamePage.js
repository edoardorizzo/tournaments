import React from "react";
import TopApp from "../components/TopApp";
import InfoMessage from "../components/InfoMessage";

function TournamentNamePage() {
  return (
    <div className="container mt-3">
      <TopApp></TopApp>
      <InfoMessage></InfoMessage>
      <input
        className="w-100 rounded-3 p-2"
        placeholder="insert tournament name..."
        type="text"
      ></input>
    </div>
  );
}

export default TournamentNamePage;
