import React from "react";
import Breadcrumb from "react-bootstrap/Breadcrumb";

const Breadcrumbs = props => {
  console.log(props);
  return (
    <Breadcrumb>
      {props.path.map(dir => {
        return (
          <Breadcrumb.Item key={Math.random()} href="#">
            {dir}
          </Breadcrumb.Item>
        );
      })}
    </Breadcrumb>
  );
};

export default Breadcrumbs;
