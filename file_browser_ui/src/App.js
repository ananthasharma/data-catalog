import React from "react";
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
        console.log(response);
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

  render() {
    return (
      <div className="App">
        <Header />
        <BreadcrumbTray path={this.state.path} getRoot={this.getRoot} />
        <FileBrowser
          list={this.state.list}
          files={this.state.files}
          onClick={this.getFolder}
          getRoot={this.getRoot}
        />
      </div>
    );
  }
}

export default App;
