import os
import json
from os import path
from django_data_catalog.CustomLogger import CustomLogger
#from django_data_catalog.CustomLogger import CustomLogger

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
        output_json = json.loads(s=output,encoding="utf-8")
        return output_json

    def list_folders(self, folder_path):
 #       self.log.debug(f"Listing contents of local folder :{folder_path}")
        output = {}
        folders = []
        files = []
        if not os._exists(folder_path):
 #           self.log.info(f"Path {folder_path} doesn't exists")
            output = {"error":f"Path {folder_path} doesn't exist"}
            print("folder not found")
            return output
        for entry in os.listdir(folder_path):
            if path.isdir(entry):
                # this is a folder
                folders.append(entry)
            if path.isfile(folder_path):
                # this is a file
                files.append(entry)
        #output.append({"name":folder_path})

LocalFSBrowser().list_folders("/")