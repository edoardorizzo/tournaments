import React from "react";
import TopApp from "../components/TopApp";
import InfoMessage from "../components/InfoMessage";
import Button from "../components/Button";

function TournamentNamePage() {
  return (
    <div className="container vh-100">
      <div className="page_element_container h-100 d-flex flex-column justify-content-between">
        <div className="top_element_container">
          <TopApp to="/" message="Tournament name"></TopApp>
          <InfoMessage caption="Inserisci il nome del tuo torneo. Ricordati di utilizzare nomi diversi
          così da non confonderti tra un torneo e l’altro, stupido Timothy."></InfoMessage>
          <input
            className="w-100 rounded-3 p-2"
            placeholder="insert tournament name..."
            type="text"
          ></input>
        </div>
        <div className="bottom_element_container mb-3">
          <Button to="/player" text="Add tournament name"></Button>
        </div>
      </div>
    </div>
  );
}

export default TournamentNamePage;
