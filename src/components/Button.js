import React from 'react';
import { Link } from "react-router-dom";

function Button({ to, text, onClick }) {
  const handleClick = () => {
    if (onClick) {
      onClick(); // Richiama l'azione passata come prop onClick
    }
  };

  return (
    <Link to={to}>
      <button className='primary_button w-100' onClick={handleClick}>
        {text}
      </button>
    </Link>
  );
}


export default Button;
