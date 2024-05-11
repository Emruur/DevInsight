import React from "react";

const Header = ( {header_name = "DevInsight"}) => {
  return (
    <div className="header">
      <div className="header-text">{header_name}</div>
    </div>
  );
};

export default Header;
