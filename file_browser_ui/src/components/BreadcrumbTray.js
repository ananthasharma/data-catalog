import React from "react";
import Dropzone from "react-dropzone";
import axios from "axios";
import Breadcrumb from "./Breadcrumb";

const BreadcrumbTray = props => (
  <div
    style={{
      display: "block",
      border: "1px solid gray",
      height: "7.5vh",
      width: "100%",
      backgroundColor: "lightGray"
    }}
  >
    <Breadcrumb path={props.path} />
    <button
      style={{
        height: "2.5vh",
        margin: "auto",
        marginRight: "1vw",
        borderRadius: "5px",
        width: "5vw"
      }}
      onClick={props.getRoot}
    >
      Root
    </button>

    <button
      style={{
        height: "2.5vh",
        margin: "auto",
        marginRight: "1vw",
        borderRadius: "5px",
        width: "5vw"
      }}
      onClick={props.goBack}
    >
      Go back
    </button>
    <button
      style={{
        height: "2.5vh",
        margin: "auto",
        marginRight: "1vw",
        borderRadius: "5px",
        width: "5vw"
      }}
      onClick={props.filterResults}
    >
      Filter
    </button>
    <Dropzone
      onDrop={acceptedFiles => {
        const file = acceptedFiles[0];
        const fileName = acceptedFiles[0].name;
        const form = new FormData();
        form.append("file_ref", file);
        form.append("file_name", fileName);
        form.append("file_location", props.path);
        axios
          .put("http://localhost:8000/files/local/list/", form)
          .then(response => {
            props.refreshStateAfterUpload(response);
          })
          .catch(error => {
            console.log(error);
          });
      }}
    >
      {({ getRootProps, getInputProps }) => (
        <button
          style={{
            height: "2.5vh",
            margin: "auto",
            marginRight: "1vw",
            borderRadius: "5px",
            width: "5vw"
          }}
          {...getRootProps()}
        >
          <input {...getInputProps()} />
          <p>Upload</p>
        </button>
      )}
    </Dropzone>
  </div>
);

export default BreadcrumbTray;
