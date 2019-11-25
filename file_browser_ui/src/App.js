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
