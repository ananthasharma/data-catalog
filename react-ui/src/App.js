import React from "react";
import axios from "axios";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";
import Navigation from "./components/Header";
import Breadcrumbs from "./components/Breadcrumbs";
import JumbotronFluid from "./components/JumbotronFluid";
import DirectoryList from "./components/DirectoryList";
const src =
  "https://www.freepik.com/free-icon/file-folder_776712.htm#page=1&query=folder&position=9";

class App extends React.Component {
  state = {
    currentPath: ["/"],
    list: [
      {
        type: "directory",
        name: "/",
        contents: [
          { type: "directory", name: "/home", contents: [] },
          { type: "directory", name: "/usr", contents: [] },
          { type: "directory", name: "/bin", contents: [] },
          { type: "directory", name: "/sbin", contents: [] },
          { type: "directory", name: "/etc", contents: [] },
          { type: "directory", name: "/var", contents: [] },
          { type: "directory", name: "/Library", contents: [] },
          { type: "directory", name: "/System", contents: [] },
          { type: "directory", name: "/.fseventsd", contents: [] },
          { type: "directory", name: "/private", contents: [] },
          { type: "directory", name: "/.vol", contents: [] },
          { type: "directory", name: "/Users", contents: [] },
          { type: "directory", name: "/Applications", contents: [] },
          { type: "directory", name: "/opt", contents: [] },
          { type: "directory", name: "/dev", contents: [] },
          { type: "directory", name: "/Volumes", contents: [] },
          { type: "directory", name: "/tmp", contents: [] },
          { type: "directory", name: "/cores", contents: [] }
        ]
      }
    ]
  };

  componentDidMount() {
    axios
      .get("http://localhost:8000/files/local/list/")
      .then(response => {
        console.log(response);
      })
      .catch(error => {
        console.log(error);
      });
  }

  getPath = event => {
    let folder = new String(event.target.innerText);
    folder = folder.slice(1);
    const currentPath = [...this.state.currentPath];
    currentPath.push(folder);
    this.setState({
      currentPath: currentPath
    });
    axios
      .get(`http://localhost:8000/files/local/list/?folder=${folder}`)
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

  render() {
    return (
      <div className="App">
        <Container>
          <Row>
            <Col sm={12}>
              <Navigation />
            </Col>
          </Row>
          <Row>
            <Col sm={12}>
              <Breadcrumbs path={this.state.currentPath} />
            </Col>
          </Row>
          <Row>
            <Col sm={2}>
              <DirectoryList list={this.state.list} getPath={this.getPath} />
            </Col>
            <Col sm={8}>
              <JumbotronFluid list={this.state.list} getPath={this.getPath} />
            </Col>
          </Row>
        </Container>
      </div>
    );
  }
}

export default App;
