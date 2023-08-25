import React from 'react';
import { Link } from "react-router-dom";

function SecondaryButton({to, text}) {
  return (
    <Link to={to}>
      <button className='secondary_button w-100 mt-2'>
        {text}
      </button>
    </Link>
    
  );
}

export default SecondaryButton;
