import React from "react";
import Jumbotron from "react-bootstrap/Jumbotron";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

const JumbotronFluid = props => {
  console.log(props);
  return (
    <Jumbotron fluid>
      <Container>
        <Row>
          {props.list[0].contents.map(dir => {
            return (
              <Col
                key={Math.random()}
                href="#"
                style={{
                  margin: "50px",
                  backgroundColor: "lightblue"
                }}
              >
                {dir.name}
              </Col>
            );
          })}
        </Row>
      </Container>
    </Jumbotron>
  );
};
export default JumbotronFluid;
