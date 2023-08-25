import React from "react";
import TopApp from "../components/TopApp";
import InfoMessage from "../components/InfoMessage";
import Button from "../components/Button";
import SecondaryButton from "../components/SecondaryButton";
import InputPlayer from "../components/InputPlayer";
import Input from "../components/Input";
import inputCounter1 from "../assets/img/input_counter1/input_counter1.svg";
import inputCounter2 from "../assets/img/input_counter1/input_counter2.svg";

function TournamentNamePage() {
  return (
    <div className="container vh-100">
      <div className="page_element_container h-100 d-flex flex-column justify-content-between">
        <div className="top_element_container">
          <div className="top_content_container mb-5">
            <TopApp to="/" message="Create tournament"></TopApp>
            <h4 className="mb-3">Insert tournament name</h4>
            <Input></Input>
            <InfoMessage
              caption="Ricordati di utilizzare nomi diversi
          così da non confonderti tra un torneo e l’altro, stupido Timothy. Questo campo è obbligatorio"
            ></InfoMessage>
          </div>

          {/* --------- */}

          <div className="bottom_content_container mb-5">
            <h4 className="mb-3">Insert players name</h4>

            <InputPlayer input={inputCounter1}></InputPlayer>
            <InputPlayer input={inputCounter2}></InputPlayer>

            <InfoMessage caption="Inserisci il nome dei giocatori presenti al torneo. il numero minimo è di due."></InfoMessage>
            <SecondaryButton text="Add player"></SecondaryButton>
          </div>
        </div>
        <div className="bottom_element_container mb-3">
          <Button text="Create tournament"></Button>
        </div>
      </div>
    </div>
  );
}

export default TournamentNamePage;
