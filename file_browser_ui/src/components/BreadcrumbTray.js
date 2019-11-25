import React from "react";
import Breadcrumb from "./Breadcrumb";

const BreadcrumbTray = props => (
  <div
    style={{
      display: "flex",
      justifyContent: "center",
      alignContent: "center",
      border: "1px solid gray",
      height: "3vh",
      backgroundColor: "lightGray"
    }}
  >
    <button
      style={{ height: "2.5vh", marginRight: "10px" }}
      onClick={props.filterResults}
    >
      Filter
    </button>
    <button
      style={{ height: "2.5vh", marginRight: "10px" }}
      onClick={props.getRoot}
    >
      Root
    </button>
    <button
      style={{ height: "2.5vh", marginRight: "10px" }}
      onClick={props.goBack}
    >
      Go back
    </button>
    <Breadcrumb path={props.path} />
  </div>
);

export default BreadcrumbTray;
