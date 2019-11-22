import React from "react";
import SvgFolderIconYellow from "../icons/FolderIconYellow";
import SvgFileIcon from "../icons/FileIcon";

const Item = props => (
  <div
    style={{
      display: "flex",
      alignItems: "center",
      padding: "20px",
      margin: "20px"
    }}
    onClick={e => props.onClick(e)}
  >
    {props.type === "directory" ? (
      <SvgFolderIconYellow width="40px" height="40px" />
    ) : props.type === "file" ? (
      <SvgFileIcon width="40px" height="40px" />
    ) : null}
    <div>{props.name}</div>
  </div>
);

export default Item;
