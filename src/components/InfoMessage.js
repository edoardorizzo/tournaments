import React from 'react'
import infoIcon from '../assets/img/info_icon.svg';

function InfoMessage() {
  return (
    <div className="d-flex justify-content-start align-items-center mb-4">
        <div className="info_container me-3">
          <img src={infoIcon} alt={infoIcon}></img>
        </div>
        <p className="p-small">
          Inserisci il nome del tuo torneo. Ricordati di utilizzare nomi diversi
          così da non confonderti tra un torneo e l’altro, stupido Timothy.
        </p>
      </div>
  )
}

export default InfoMessage