import React from "react";
import Jumbotron from "react-bootstrap/Jumbotron";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

const JumbotronFluid = props => {
  console.log(props);
  return (
    // <Jumbotron fluid>
    //   <Container>
    //     <Row>
    <div>
      {!props.list === []
        ? props.list.map(dir => {
            return (
              <Col
                key={Math.random()}
                href="#"
                style={{
                  margin: "50px",
                  backgroundColor: "lightblue"
                }}
                onClick={e => props.getPath(e)}
              >
                {dir.name}
              </Col>
            );
          })
        : null}
    </div>
    //   </Row>
    // </Container>
    // </Jumbotron>
  );
};
export default JumbotronFluid;
