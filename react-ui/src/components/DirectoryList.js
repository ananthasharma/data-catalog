import React from "react";
import Nav from "react-bootstrap/Nav";
import Jumbotron from "react-bootstrap/Jumbotron";

const DirectoryList = props => {
  console.log(props.list[0].contents);
  return (
    <Jumbotron>
      <Nav defaultActiveKey="/home" className="flex-column">
        {props.list[0].contents.map(directory => {
          return (
            <Nav.Link
              key={Math.random()}
              id={directory.name}
              href="#"
              onClick={e => props.getPath(e)}
            >
              {directory.name}
            </Nav.Link>
          );
        })}
      </Nav>
    </Jumbotron>
  );
};

export default DirectoryList;
