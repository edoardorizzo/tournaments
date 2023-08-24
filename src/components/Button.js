import React from 'react';
import { Link } from "react-router-dom";

function Button() {
  return (
    <Link to="/tournament">
      <button className='primary_button'>
        Start Tournament
      </button>
    </Link>
    
  );
}

export default Button;
