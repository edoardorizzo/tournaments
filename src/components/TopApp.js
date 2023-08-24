import React from 'react'
import backArrow from "../assets/img/back_arrow.svg";


function TopApp() {
  return (
    <div className="top_app d-flex align-items-center mb-4">
        <div className="arrow_container me-5">
          <img src={backArrow} alt={backArrow}></img>
        </div>
        <h4>Tournament Name</h4>
    </div>
  )
}

export default TopApp