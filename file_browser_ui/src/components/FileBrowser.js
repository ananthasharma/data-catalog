import React from "react";
import Item from "./Item.js";

const FileBrowser = props => (
  <div
    style={{
      display: "flex",
      flexWrap: "wrap",
      justifyContent: "space-evenly",
      width: "65%",
      margin: "auto"
    }}
  >
    {props.list.length !== 0 ? (
      props.list.map(item => {
        return (
          <Item
            key={Math.random()}
            type={item.type}
            name={item.name}
            onClick={props.onClick}
          />
        );
      })
    ) : (
      <div
        style={{
          display: "block",
          margin: "auto"
        }}
      >
        <p>
          There are no folders or files in this path. Click to go back to root.
        </p>
        <button style={{ height: "25px" }} onClick={props.getRoot}>
          Root
        </button>
      </div>
    )}
  </div>
);

export default FileBrowser;
