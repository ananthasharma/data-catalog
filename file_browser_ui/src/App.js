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
    list: []
  };

  componentDidMount() {
    this.getRoot();
  }

  getRoot = () => {
    axios
      .get("http://localhost:8000/files/local/list/")
      .then(response => {
        this.setState({
          path: response.data[0].name,
          list: response.data[0].contents
        });
      })
      .catch(error => {
        console.log(error);
      });
  };

  getFolder = event => {
    const folder = event.target.innerText;
    axios
      .get(`http://localhost:8000/files/local/list/?folder=${folder}`)
      .then(response => {
        this.setState({
          path: response.data[0].name,
          list: response.data[0].contents
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
        <BreadcrumbTray path={this.state.path} />
        <FileBrowser
          list={this.state.list}
          onClick={this.getFolder}
          getRoot={this.getRoot}
        />
      </div>
    );
  }
}

export default App;
