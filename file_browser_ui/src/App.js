import React from "react";
import fileDownload from "js-file-download";
import axios from "axios";
import "./App.css";

import Header from "./components/Header";
import BreadcrumbTray from "./components/BreadcrumbTray";
import FileBrowser from "./components/FileBrowser";
import FileUpload from "./components/FileUpload";

class App extends React.Component {
  state = {
    path: [],
    list: [],
    files: [],
    fileToUpload: null
  };

  componentDidMount() {
    this.getRoot();
  }

  getRoot = () => {
    axios
      .get("http://localhost:8000/files/local/list/")
      .then(response => {
        const path = response.data[0].name;
        let list = [];
        let files = [];
        response.data[0].contents.forEach(index => {
          if (Array.isArray(index)) {
            index.forEach(i => {
              files.push(i);
            });
          } else {
            list.push(index);
          }
        });
        this.setState({
          path,
          list,
          files
        });
      })
      .catch(error => {
        console.log(error);
      });
  };

  getFolder = folder => {
    axios
      .get(`http://localhost:8000/files/local/list/?folder=${folder}`)
      .then(response => {
        const path = response.data[0].name;
        let list = [];
        let files = [];
        response.data[0].contents.forEach(index => {
          if (Array.isArray(index)) {
            index.forEach(i => {
              files.push(i);
            });
          } else {
            list.push(index);
          }
        });
        this.setState({
          path,
          list,
          files
        });
      })
      .catch(error => {
        console.log(error);
      });
  };

  downloadFile = filePath => {
    axios
      .get(`http://localhost:8000/files/local/download/?file_path=${filePath}`)
      .then(response => {
        fileDownload(response.data, `${filePath}`);
      })
      .catch(error => {
        console.log(error);
      });
  };

  handleFileUpload = event => {
    console.log(event.target);
    console.log(event.target.files[0]);
    const file = event.target.files[0];
    const data = new FormData();
    data.append("file", file);
    console.log(data);
    axios
      .put("http://0.0.0.0:8000/files/local/list/", file)
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
        <Header />
        <BreadcrumbTray path={this.state.path} getRoot={this.getRoot} />
        <input
          style={{
            margin: "auto",
            height: "50px",
            width: "50px",
            border: "1px solid black",
            backgroundColor: " gray"
          }}
          type="file"
          name="file"
          onChange={this.handleFileUpload}
        ></input>
        <FileBrowser
          list={this.state.list}
          files={this.state.files}
          getRoot={this.getRoot}
          getFolder={this.getFolder}
          downloadFile={this.downloadFile}
        />
        <FileUpload />
      </div>
    );
  }
}

export default App;
