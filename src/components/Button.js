import React from 'react';
import { Link } from "react-router-dom";

function Button({to, text}) {
  return (
    <Link to={to}>
      <button className='primary_button w-100'>
        {text}
      </button>
    </Link>
    
  );
}

export default Button;
