import React from "react";
import SvgFolderIconYellow from "../icons/FolderIconYellow";

const Header = () => (
  <div
    style={{
      display: "flex",
      justifyContent: "center",
      alignItems: "center",
      height: "5vh",
      width: "100%",
      margin: "auto",
      border: "1px solid gray",
      backgroundColor: "lightBlue"
    }}
  >
    <SvgFolderIconYellow width="40px" height="40px" />
    <div>File System Browser</div>
  </div>
);

export default Header;
