import React from "react";
import fileDownload from "js-file-download";
import Dropzone from "react-dropzone";
import axios from "axios";
import "./App.css";

import Header from "./components/Header";
import BreadcrumbTray from "./components/BreadcrumbTray";
import FileBrowser from "./components/FileBrowser";

class App extends React.Component {
  state = {
    path: "",
    list: [],
    sortedList: [],
    showList: [],
    files: [],
    sortedFiles: [],
    showFiles: [],
    showFilterMenu: false,
    sortOrder: "a - z",
    isSorted: false,
    foldersOnly: false,
    filesOnly: false
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
        let showList = [];
        let files = [];
        let showFiles = [];
        response.data[0].contents.forEach(index => {
          if (Array.isArray(index)) {
            index.forEach(i => {
              files.push(i);
              showFiles.push(i);
            });
          } else {
            list.push(index);
            showList.push(index);
          }
        });
        this.setState({
          path,
          list,
          showList,
          files,
          showFiles
        });
      })
      .catch(error => {
        console.log(error);
      });
  };

  goBack = () => {
    const path = this.state.path;
    const removeSlash = path.slice(0, path.length - 1);
    const index = removeSlash.lastIndexOf("/");
    let slicePath;
    if (index !== path.length - 1) {
      slicePath = path.slice(0, index + 1);
    }
    this.getFolder(slicePath);
  };

  getFolder = folder => {
    axios
      .get(`http://localhost:8000/files/local/list/?folder=${folder}`)
      .then(response => {
        let path = response.data[0].name;
        if (!path.endsWith("/")) {
          path = path + "/";
        }
        let list = [];
        let showList = [];
        let files = [];
        let showFiles = [];
        response.data[0].contents.forEach(index => {
          if (Array.isArray(index)) {
            index.forEach(i => {
              files.push(i);
              showFiles.push(i);
            });
          } else {
            list.push(index);
            showList.push(index);
          }
        });
        this.setState({
          path,
          list,
          showList,
          files,
          showFiles
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

  filterResults = () => {
    const isActive = this.state.showFilterMenu;
    this.setState({ showFilterMenu: !isActive });
  };

  sortResults = () => {
    const list = [...this.state.list];
    const files = [...this.state.files];
    if (this.state.sortOrder === "a - z") {
      const sortedList = list.sort(function(a, b) {
        if (a.name > b.name) {
          return 1;
        }
        if (a.name < b.name) {
          return -1;
        }
        return 0;
      });
      const sortedFiles = files.sort(function(a, b) {
        if (a.name > b.name) {
          return 1;
        }
        if (a.name < b.name) {
          return -1;
        }
        return 0;
      });
      this.setState({
        sortedList,
        sortedFiles,
        showList: sortedList,
        showFiles: sortedFiles,
        sortOrder: "z - a",
        isSorted: true
      });
    } else if (this.state.sortOrder === "z - a") {
      const sortedList = list.sort(function(a, b) {
        if (a.name < b.name) {
          return 1;
        }
        if (a.name > b.name) {
          return -1;
        }
        return 0;
      });
      const sortedFiles = files.sort(function(a, b) {
        if (a.name < b.name) {
          return 1;
        }
        if (a.name > b.name) {
          return -1;
        }
        return 0;
      });
      this.setState({
        sortedList,
        sortedFiles,
        showList: sortedList,
        showFiles: sortedFiles,
        sortOrder: "a - z",
        isSorted: true
      });
    }
  };

  foldersOnly = () => {
    let list, files;
    if (this.state.isSorted) {
      list = [...this.state.sortedList];
      files = [...this.state.sortedFiles];
    } else {
      list = [...this.state.list];
      files = [...this.state.files];
    }
    if (!this.state.foldersOnly) {
      this.setState({
        showFiles: [],
        showList: list,
        foldersOnly: true,
        filesOnly: false
      });
    } else if (this.state.foldersOnly) {
      this.setState({
        showFiles: files,
        showList: list,
        foldersOnly: false,
        filesOnly: false
      });
    }
  };

  filesOnly = () => {
    let list, files;
    if (this.state.isSorted) {
      list = [...this.state.sortedList];
      files = [...this.state.sortedFiles];
    } else {
      list = [...this.state.list];
      files = [...this.state.files];
    }
    if (!this.state.filesOnly) {
      this.setState({
        showList: [],
        showFiles: files,
        filesOnly: true,
        foldersOnly: false
      });
    } else if (this.state.filesOnly) {
      this.setState({
        showList: list,
        showFiles: files,
        filesOnly: false,
        foldersOnly: false
      });
    }
  };

  clearAll = () => {
    const list = [...this.state.list];
    const files = [...this.state.files];
    this.setState({
      showList: list,
      showFiles: files,
      sortOrder: "a - z",
      isSorted: false,
      foldersOnly: false,
      filesOnly: false
    });
  };

  render() {
    return (
      <div className="App">
        <Header />
        <BreadcrumbTray
          path={this.state.path}
          getRoot={this.getRoot}
          goBack={this.goBack}
          filterResults={this.filterResults}
        />
        {this.state.showFilterMenu ? (
          <div
            style={{
              display: "flex",
              height: "2.5vh",
              justifyContent: "center",
              border: "1px solid gray",
              backgroundColor: "lightGray"
            }}
          >
            <button onClick={this.sortResults}>
              Sort {this.state.sortOrder}
            </button>
            <button onClick={this.foldersOnly}>
              {this.state.foldersOnly ? (
                <strong>Folders Only</strong>
              ) : (
                <p>Folders Only</p>
              )}
            </button>
            <button onClick={this.filesOnly}>
              {this.state.filesOnly ? (
                <strong>Files Only</strong>
              ) : (
                <p>Files Only</p>
              )}
            </button>
            <button onClick={this.clearAll}>Clear All</button>
          </div>
        ) : null}
        <FileBrowser
          list={this.state.showList}
          files={this.state.showFiles}
          getFolder={this.getFolder}
          downloadFile={this.downloadFile}
          getRoot={this.getRoot}
        />
        <Dropzone
          onDrop={acceptedFiles => {
            const file = acceptedFiles[0];
            const fileName = acceptedFiles[0].name;
            const form = new FormData();
            form.append("file_ref", file);
            form.append("file_name", fileName);
            form.append("file_location", "/tmp/folder5/");
            axios
              .put("http://0.0.0.0:8000/files/local/list/", form)
              .then(response => {
                console.log(response);
              })
              .catch(error => {
                console.log(error);
              });
          }}
        >
          {({ getRootProps, getInputProps }) => (
            <section
              style={{
                display: "block",
                margin: "auto",
                marginTop: "20px",
                width: "50%",
                height: "50px",
                border: "1px dotted black",
                backgroundColor: "lightGray"
              }}
            >
              <div {...getRootProps()}>
                <input {...getInputProps()} />
                <p>Drag 'n' drop some files here, or click to select files</p>
              </div>
            </section>
          )}
        </Dropzone>
      </div>
    );
  }
}

export default App;
