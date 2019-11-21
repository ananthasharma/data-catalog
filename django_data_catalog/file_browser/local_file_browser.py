import os
import json
from os import path
from django_data_catalog.CustomLogger import CustomLogger


# from django_data_catalog.CustomLogger import CustomLogger

class LocalFSBrowser:
    log = CustomLogger.logger

    def list_using_tree(self, folder_path):
        """ list folders and files using the tree command
        tree -J --dirsfirst -L 1 <<folder_path>>
         """
        self.log.debug(f"Listing contents of local folder :{folder_path}")

        str_shell_command = f"tree -J --dirsfirst -L 1 {folder_path}"

        self.log.debug(f"running command {str_shell_command}")

        stream = os.popen(str_shell_command)
        output = stream.read()
        self.log.debug(f"json of size : {len(output)} will be returned.")
        output_json = json.loads(s=output, encoding="utf-8")
        return output_json

    def list_folders(self, folder_path):
        # self.log.debug(f"Listing contents of local folder :{folder_path}")
        output = []
        folders = []
        files = []
        if not os.path.exists(folder_path):
            output.append({"name": f"{folder_path}", "contents": [{"error": "opening dir"}]})
            print("folder not found")
            return output
        for entry in os.listdir(path=folder_path):
            if not folder_path.endswith("/"):
                folder_path = folder_path + "/"
            entry = folder_path + entry
            if path.isdir(entry):
                # this is a folder
                folders.append({"type": "directory", "name": entry, "contents": []})
            if path.isfile(folder_path):
                # this is a file
                files.append({"type": "file", "name": entry})
        self.log.debug(f"found {len(folders)} folder and {len(files)} files")
        folders.extend(files)
        output.append({"type": "directory", "name": folder_path, "contents": folders})
        return output


LocalFSBrowser().list_folders("/")
