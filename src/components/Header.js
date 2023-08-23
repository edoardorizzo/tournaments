import React from "react";
import Logo from "../assets/img/Logo.svg";

function Header() {
  return (
    <header>
      <div className="header_logo mt-3">
        <img src={Logo} alt={Logo}></img>
      </div>
    </header>
  );
}

export default Header;
