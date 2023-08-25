import React, { useState } from "react";
import TopApp from "../components/TopApp";
import InfoMessage from "../components/InfoMessage";
import Button from "../components/Button";
import SecondaryButton from "../components/SecondaryButton";
import InputPlayer from "../components/InputPlayer";
import Input from "../components/Input";
import inputCounter1 from "../assets/img/input_counter1/input_counter1.svg";
import inputCounter2 from "../assets/img/input_counter1/input_counter2.svg";
import inputCounter3 from "../assets/img/input_counter1/input_counter3.svg";
import inputCounter4 from "../assets/img/input_counter1/input_counter4.svg";


function TournamentNamePage() {
  const [players, setPlayers] = useState([inputCounter1, inputCounter2]);
  const [clickCount, setClickCount] = useState(1);

  const addPlayer = () => {
    if (clickCount <= 18) {
      setPlayers([...players, `inputCounter${clickCount + 2}`]);
      setClickCount(clickCount + 1);
    }
  };

  return (
    <div className="container vh-100">
      <div className="page_element_container h-100 d-flex flex-column justify-content-between">
        <div className="top_element_container">
          <div className="top_content_container mb-5">
            <TopApp to="/" message="Create tournament" />
            <h4 className="mb-3">Insert tournament name</h4>
            <Input />
            <InfoMessage
              caption="Ricordati di utilizzare nomi diversi così da non confonderti tra un torneo e l’altro, stupido Timothy. Questo campo è obbligatorio"
            />
          </div>

          <div className="bottom_content_container mb-5">
            <h4 className="mb-3">Insert players name</h4>
            <ul>
              {players.map((playerInput, index) => (
                <li key={index}>
                  <InputPlayer input={playerInput} />
                </li>
              ))}
            </ul>
            <InfoMessage caption="Inserisci il nome dei giocatori presenti al torneo. Il numero minimo è di due." />
            <SecondaryButton text="Add player" onClick={addPlayer} />
          </div>
        </div>
        <div className="bottom_element_container mb-3">
          <Button text="Create tournament" />
        </div>
      </div>
    </div>
  );
}

export default TournamentNamePage;
