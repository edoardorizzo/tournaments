import React from 'react';

function SecondaryButton({ text, onClick }) {
  return (
    <button className='secondary_button w-100 mt-2' onClick={onClick}>
      {text}
    </button>
  );
}

export default SecondaryButton;
