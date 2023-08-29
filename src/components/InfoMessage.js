import React from 'react'
import infoIcon from '../assets/img/info_icon.svg';

function InfoMessage( { caption }) {
  return (
    <div className="d-flex justify-content-start align-items-center">
        <div className="info_container me-3">
          <img src={infoIcon} alt={infoIcon}></img>
        </div>
        <p className="p-small">
          {caption}
        </p>
      </div>
  )
}

export default InfoMessage