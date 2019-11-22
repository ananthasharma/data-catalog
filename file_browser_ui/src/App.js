import React from "react";
import fileDownload from "js-file-download";
import axios from "axios";
import logo from "./logo.svg";
import "./App.css";

import Header from "./components/Header";
import BreadcrumbTray from "./components/BreadcrumbTray";
import FileBrowser from "./components/FileBrowser";
import SvgFolderIconYellow from "./icons/FolderIconYellow";

class App extends React.Component {
  state = {
    path: [],
    list: [],
    files: []
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

  render() {
    return (
      <div className="App">
        <Header />
        <BreadcrumbTray path={this.state.path} getRoot={this.getRoot} />
        <FileBrowser
          list={this.state.list}
          files={this.state.files}
          getRoot={this.getRoot}
          getFolder={this.getFolder}
          downloadFile={this.downloadFile}
        />
      </div>
    );
  }
}

export default App;
