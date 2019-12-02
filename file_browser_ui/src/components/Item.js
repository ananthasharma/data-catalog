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
    onClick={
      props.getFolder
        ? () => props.getFolder(props.name)
        : () => props.downloadFile(props.name)
    }
  >
    {props.type === "directory" ? (
      <SvgFolderIconYellow width="5vw" height="5vh" />
    ) : props.type === "file" ? (
      <SvgFileIcon width="4vw" height="4vh" />
    ) : null}
    <div>{props.name}</div>
  </div>
);

export default Item;
