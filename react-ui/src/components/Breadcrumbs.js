import React from "react";
import Breadcrumb from "react-bootstrap/Breadcrumb";

const Breadcrumbs = props => {
  return (
    // <Breadcrumb>
    <div>
      {props.update
        ? props.path.map(dir => {
            return (
              // <Breadcrumb.Item key={Math.random()} href="#">
              <div>  
              {dir}
              </div>
              // </Breadcrumb.Item>
            );
          })
        : null}
        </div>
    /* </Breadcrumb> */
  );
};

export default Breadcrumbs;
