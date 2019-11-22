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

    def list_folders(self, folder_path, depth=1):
        #       self.log.debug(f"Listing contents of local folder :{folder_path}")
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
            if path.isfile(entry):
                # this is a file
                files.append({"type": "file", "name": entry})
        depth = depth - 1  # decrement, because we've looked at 1 level already
        for iterations in range(1, depth):
            # iterate through folders until depth is zero.
            # TODO: Implement this feature (at some point in the future)
            pass

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
        os.mkdir(path=dir_name) # create the folder; if it exists, nothing changes; if it doesn't create it
        if not os.path.exists(dir_name):
            # Alas! our attempt to create a folder has failed; we cannot store a file in a non existent folder.
            # lets stop here.
            raise IOError("Unable to create folder")

        if os.path.exists(target_file_name):
            """file already exists with this name"""
            # TODO: check if the user has the ability to overwrite this file

        # assuming the user has the role to store this file in this location
        try:
            # write to the file at destination
            with open(target_file_name, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
        except IOError:
            # whenever something bad happens while writing to the file
            self.log.debug(f"trouble writing to location {target_file_name}")
            return False

        return True
