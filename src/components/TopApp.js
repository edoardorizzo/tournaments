import React from 'react'
import backArrow from "../assets/img/back_arrow.svg";
import { Link } from 'react-router-dom';


function TopApp( {to, message} ) {
  return (
    <div className="top_app d-flex align-items-center mt-3 mb-4">
        <Link to={to}>
        <div className="arrow_container me-5">
          <img src={backArrow} alt={backArrow}></img>
        </div>
        </Link>
        <h3>{message}</h3>
    </div>
  )
}

export default TopApp