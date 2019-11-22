import React from "react";
import Nav from "react-bootstrap/Nav";
import Jumbotron from "react-bootstrap/Jumbotron";

const DirectoryList = props => {
  return (
    <Jumbotron>
      <Nav defaultActiveKey="/home" className="flex-column">
        {!props.list === []
          ? props.list.map(directory => {
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
            })
          : null}
      </Nav>
    </Jumbotron>
  );
};

export default DirectoryList;
