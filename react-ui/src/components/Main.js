import React from "react";
import axios from "axios";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import "bootstrap/dist/css/bootstrap.min.css";

import Navigation from "./Header";
import Breadcrumbs from "./Breadcrumbs";
import JumbotronFluid from "./JumbotronFluid";
import DirectoryList from "./DirectoryList";
const src =
  "https://www.freepik.com/free-icon/file-folder_776712.htm#page=1&query=folder&position=9";

class Main extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      update: false,
      currentPath: [],
      list: []
    };
  }

  componentDidMount() {
    axios
      .get("http://localhost:8000/files/local/list/")
      .then(response => {
        console.log(response);
        const currentPath = response.data[0].name;
        const currentList = response.data[0].contents;
        this.setState({
          update: true,
          currentPath: currentPath,
          list: currentList
        });
      })
      .catch(error => {
        console.log(error);
      });
  }

  getPath = event => {
    const rawFolder = event.target.innerText;
    let folder = new String(event.target.innerText);
    folder = folder.slice(1);
    const currentPath = [...this.state.currentPath];
    currentPath.push(folder);
    this.setState({
      currentPath: currentPath
    });
    axios
      .get(`http://localhost:8000/files/local/list/?folder=${rawFolder}`)
      .then(response => {
        console.log(response);
      })
      .catch(error => {
        console.log(error);
      });
  };

  getFileForDownload = filePath => {
    console.log(filePath);
    axios
      .get(`http://localhost:8000/files/local/download/?file_path=${filePath}`)
      .then(response => {
        console.log(response);
      })
      .catch(error => {
        console.log(error);
      });
  };

  render = () => {
    return (
      <div className="Main">
        <Container>
          <Row>
            <Col sm={12}>
              <Navigation />
            </Col>
          </Row>
          <Row>
            <Col sm={12}>
              <Breadcrumbs
                update={this.state.update}
                path={this.state.currentPath}
              />
            </Col>
          </Row>
          <Row>
            <Col sm={2}>
              <DirectoryList
                update={this.state.update}
                list={this.state.list}
                getPath={this.getPath}
              />
            </Col>
            <Col sm={8}>
              <JumbotronFluid
                update={this.state.update}
                list={this.state.list}
                getPath={this.getPath}
              />
            </Col>
          </Row>
        </Container>
      </div>
    );
  };
}

export default Main;
