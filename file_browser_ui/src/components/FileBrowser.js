import React from "react";
import Item from "./Item.js";

const FileBrowser = props => {
  console.log(props);
  return (
    <div
      style={{
        display: "flex",
        flexWrap: "wrap",
        justifyContent: "space-evenly",
        height: "75vh",
        width: "50vw",
        margin: "auto"
      }}
    >
      {props.list.length
        ? props.list.map(item => {
            return (
              <Item
                key={Math.random()}
                type={item.type}
                name={item.name}
                getFolder={props.getFolder}
              />
            );
          })
        : null}
      {props.files.length
        ? props.files.map(item => {
            console.log(item);
            return (
              <Item
                key={Math.random()}
                type={item.type}
                name={item.name}
                downloadFile={props.downloadFile}
              />
            );
          })
        : null}
      {!props.list.length && !props.files.length ? (
        <div
          style={{
            display: "block",
            margin: "auto"
          }}
        >
          <p>
            There are no folders or files in this path. Click to go back to
            root.
          </p>
          <button
            style={{
              height: "2.5vh",
              margin: "auto",
              marginRight: "1vw",
              borderRadius: "5px",
              width: "5vw",
              backgroundColor: "lightGray"
            }}
            onClick={props.getRoot}
          >
            Root
          </button>
        </div>
      ) : null}
    </div>
  );
};

export default FileBrowser;
