import React from "react";
import Breadcrumb from "./Breadcrumb";

const BreadcrumbTray = props => (
  <div
    style={{
      border: "1px solid gray",
      height: "2.5vh",
      backgroundColor: "lightGray"
    }}
  >
    <Breadcrumb path={props.path} />
  </div>
);

export default BreadcrumbTray;
