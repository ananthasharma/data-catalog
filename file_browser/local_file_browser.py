import os
import json
from os import path
from pathlib import Path
from core.CustomLogger import CustomLogger


class LocalFSBrowser:
    log = CustomLogger.logger

    def list_folders(self, folder_path: str):
        self.log.debug(f"Listing contents of local folder :{folder_path}")
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
            if ".." in entry:
                # the entry contains reference to parent folder.
                # we need to stop this call
                raise ValueError({"error": "reference to parent folder isn't allowed (basically no '..')"})

            if path.isdir(entry):
                # this is a folder
                folders.append({"type": "directory", "name": entry, "contents": []})
            if path.isfile(entry):
                # this is a file
                path_instance = Path(entry)
                size = os.stat(entry).st_size
                files.append({"type": "file", "name": entry, "simple_name": path_instance.name, "file_size": size})

        self.log.debug(f"found {len(folders)} folder and {len(files)} files")
        folders.append(files)
        output.append({"type": "directory", "name": folder_path, "contents": folders})

        return output

    def store_file(self, file, dir_name, file_name) -> bool:
        """stores an uploaded file into a location
        :type file: File
        :type dir_name: string
        :type file_name: string
        """

        if not dir_name.endswith("/"):
            dir_name = dir_name + "/"

        target_file_name = dir_name + file_name;

        self.log.debug(f"saving to {target_file_name}")

        if not os.path.exists(dir_name):
            # create the folder
            self.log.debug(f"folder {dir_name} doesn't yet exist. creating it now")
            os.mkdir(path=dir_name)
        else:
            self.log.debug(f"folder {dir_name} already exists")

        if os.path.exists(target_file_name):
            """file already exists with this name"""
            # TODO: check if the user has the ability to overwrite this file
            # also, is this check needed?
            self.log.error(f"File: {target_file_name} already exists")
            raise IOError("File already exists, cannot overwrite.")
        # assuming the user has the role to store this file in this location
        try:
            # here, the
            # 1. User has rights to write into provided path
            # 2. Another file with the same name doesn't already exist here
            # 3.
            # write to the file at destination
            self.log.debug(f"opening file {target_file_name} for writing")
            with open(target_file_name, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
                self.log.debug(f"writing to file {target_file_name} successful")
        except IOError:
            # whenever something bad happens while writing to the file
            self.log.debug(f"trouble writing to location {target_file_name}")
            raise IOError(f"trouble writing to location {target_file_name}")

        return True