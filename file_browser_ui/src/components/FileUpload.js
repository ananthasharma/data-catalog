import React, { useState } from "react";
import ReactDOM from "react-dom";
// Import React FilePond
import { FilePond, File, registerPlugin } from "react-filepond";

// Import FilePond styles
import "filepond/dist/filepond.min.css";

// Import the Image EXIF Orientation and Image Preview plugins
// Note: These need to be installed separately
// `npm i filepond-plugin-image-preview filepond-plugin-image-exif-orientation --save`
import FilePondPluginImageExifOrientation from "filepond-plugin-image-exif-orientation";
import FilePondPluginImagePreview from "filepond-plugin-image-preview";
import "filepond-plugin-image-preview/dist/filepond-plugin-image-preview.css";

// Register the plugins
registerPlugin(FilePondPluginImageExifOrientation, FilePondPluginImagePreview);

const FileUpload = props => {
  const [files, setFiles] = useState([]);
  return (
    <div className="App">
      <FilePond
        server={{
          url: 'http://localhost:8000/files/local/list/',
          method: "PATCH",
        //   headers: {
        //     "Accept": "*/*",
        //     "Accept-Encoding": "gzip, deflate",
        //     "Cache-Control": "no-cache",
        //     "Connection": "keep-alive",
        //     "Content-Length": "4420811",
        //     "Content-Type": "application/x-www-form-urlencoded",
        //     "Host": "0.0.0.0:8000",
        //     "Postman-Token":
        //       "462c9038-2e3d-4764-a36e-46e50931118c,9f5dff71-6675-43f9-872b-fcf4997c8202",
        //     "User-Agent": "PostmanRuntime/7.19.0",
        //     "cache-control": "no-cache",
        //     "content-type":
        //       "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW"
        //   }
        }}
        files={files}
        allowMultiple={true}
        onupdatefiles={setFiles}
        labelIdle='Drag & Drop your files or <span class="filepond--label-action">Browse</span>'
      />
    </div>
  );
};

export default FileUpload;
