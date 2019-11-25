import React from "react";
import Breadcrumb from "./Breadcrumb";

const BreadcrumbTray = props => (
  <div
    style={{
      display: "flex",
      justifyContent: "center",
      border: "1px solid gray",
      height: "2.5vh",
      backgroundColor: "lightGray"
    }}
  >
    <button style={{ marginRight: "5px" }} onClick={props.getRoot}>
      Root
    </button>
    <button style={{marginRight: "5px"}} onClick={props.goBack}>
      Go back
    </button>
    <Breadcrumb path={props.path} />
  </div>
);

export default BreadcrumbTray;
