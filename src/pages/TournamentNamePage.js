import React, { useState } from "react";
import TopApp from "../components/TopApp";
import InfoMessage from "../components/InfoMessage";
import Button from "../components/Button";
import SecondaryButton from "../components/SecondaryButton";
import InputPlayer from "../components/InputPlayer";
import Input from "../components/Input";
import InputPlayerDelete from "../components/InputPlayerDelete";
import userIcon from "../assets/img/user-solid.svg";

function TournamentNamePage() {
  const [tournamentName, setTournamentName] = useState(""); // Stato per il nome del torneo
  const [playerNames, setPlayerNames] = useState(["", ""]); // Stato per i nomi dei giocatori

  const [clickCount, setClickCount] = useState(1);
  const [addedPlayers, setAddedPlayers] = useState([]);

  const addPlayer = () => {
    if (clickCount <= 18) {
      setAddedPlayers([...addedPlayers, `inputCounter${clickCount + 2}`]);
      setClickCount(clickCount + 1);
    }
  };

  const removePlayer = (indexToRemove) => {
    const updatedPlayers = addedPlayers.filter(
      (_, index) => index !== indexToRemove
    );
    setAddedPlayers(updatedPlayers);
  };

  const handlePlayerNameChange = (index, value) => {
    const updatedPlayerNames = [...playerNames];
    updatedPlayerNames[index] = value;
    setPlayerNames(updatedPlayerNames);
  };

  const createTournament = () => {
    // Crea l'oggetto con i dati raccolti
    const tournamentData = {
      tournamentName,
      playerNames,
    };

    console.log("Tournament data:", tournamentData);

    // Qui puoi eseguire ulteriori azioni come inviare i dati al server, ecc.
  };

  return (
    <div className="container vh-100">
      <div className="page_element_container h-100 d-flex flex-column justify-content-between">
        <div className="top_element_container">
          <div className="top_content_container mb-5">
            <TopApp to="/" message="Create tournament" />
            <h4 className="mb-3">Insert tournament name</h4>
            <Input
              value={tournamentName}
              onChange={(e) => setTournamentName(e.target.value)}
            />
            <InfoMessage caption="Ricordati di utilizzare nomi diversi così da non confonderti tra un torneo e l’altro, stupido Timothy. Questo campo è obbligatorio" />
          </div>

          <div className="bottom_content_container mb-5">
            <h4 className="mb-3">Insert players name</h4>
            <ul>
              <li>
                <InputPlayer
                  input={userIcon}
                  playerName={playerNames[0] || ""}
                  onChange={(e) => handlePlayerNameChange(0, e.target.value)}
                />
              </li>
              <li>
                <InputPlayer
                  input={userIcon}
                  playerName={playerNames[1] || ""}
                  onChange={(e) => handlePlayerNameChange(1, e.target.value)}
                />
              </li>
              {addedPlayers.map((player, index) => (
                <li key={index}>
                  <InputPlayerDelete
                    input={userIcon}
                    playerName={playerNames[index + 2] || ""}
                    onRemove={() => removePlayer(index)}
                    onChange={(e) =>
                      handlePlayerNameChange(index + 2, e.target.value)
                    }
                  />
                </li>
              ))}
            </ul>
            <InfoMessage caption="Inserisci il nome dei giocatori presenti al torneo. Il numero minimo è di due." />
            <SecondaryButton text="Add player" onClick={addPlayer} />
          </div>
        </div>
        <div className="bottom_element_container mb-3">
          <Button text="Create tournament" onClick={createTournament} to="/matches"/>
        </div>
      </div>
    </div>
  );
}

export default TournamentNamePage;
