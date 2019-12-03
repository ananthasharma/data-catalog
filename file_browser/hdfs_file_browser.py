import os

from core.CustomLogger import CustomLogger
from django.conf import settings


class HDFSCommandLineFileBrowser:
    #    lan_config = settings.LAN_FOLDER_CONFIG
    lan_config = [
        # populate this list for testing; use settings.LAN_FOLDER_CONFIG in dev & higher env.
        {"root": "/LAN34", "actual_path": "/opt"},
        {"root": "/LAN33", "actual_path": "/var"},
        {"root": "/LAN35", "actual_path": "/usr"},
        {"root": "/LAN36", "actual_path": "/opt/mapr"},
    ]
    log = CustomLogger.logger

    def __init__(self):
        pass

    def list_files(self, folder_path: str) -> [str]:
        """Lists files using a shell command
        approach::
        use hdfs dfs -ls <<folder path>> command to list all folders and files; call this output
        use hdfs dfs -ls -C <<folder path>> command to list only file or folder names; call this output_names
        **** it is assumed that nothing changed in the folders between these two commands running ****
        split each entry in output by line; remove matching names from output_names (as they are in the same order);
        figure out of the entry is a file or folder by checking if entries in output starts with "d"
        prepare response

        Args:
            folder_path: str (path to a folder to list files from
        """
        self.log.debug(f"service invoked for folder :{folder_path}")
        folder_path = self.decode(folder_path)  # decode
        hdp_command = f"{settings.HADOOP_COMMAND_LOCATION} dfs -ls {folder_path}"
        hdp_names_only_command = f"{settings.HADOOP_COMMAND_LOCATION} dfs -ls -C {folder_path}"
        self.log.info(f"running command '{hdp_command}'")
        output = os.popen(hdp_command).read()
        # self.log.debug(f"\n\n\n\n {hdp_command} \n got response {output}")
        self.log.info(f"running command '{hdp_names_only_command}'")
        output_names = os.popen(hdp_names_only_command).read()
        # self.log.debug(f"\n\n\n\n {hdp_names_only_command} \n got response {output_names}")

        response = []
        # this only lists the file and folder names.. we can continue
        names_as_array = output_names.splitlines()

        # the first line is always the count of entries, we need to ignore it
        listings_as_array = output.splitlines()[1:]

        if len(listings_as_array) == 0:
            response.append({"type": "directory", "name": folder_path, "contents": []})
            return response

        for idx, entry in enumerate(listings_as_array):
            # encode
            abs_path = self.encode(names_as_array[idx])
            file_name = abs_path.split("/").pop()
            if str(entry).startswith("d"):
                # then names_as_array[idx] is a folder
                response.append(
                    {"type": "directory", "name": abs_path, "simple_name": file_name, "contents": []})
            else:
                # extract the last elem
                # "['drwx------   - asharma staff         64 2019-12-01 20:54 .Trash']"
                # when we replace "<blank space> file name" with blank we get
                # "['drwx------   - asharma staff         64 2019-12-01 20:54']"
                # we need to split this into an array separated by space, then we get
                # ['drwx------', '', '', '-', 'asharma', 'staff', '', '', '', '', '', '', '', '', '64', '2019-12-01', '20:54']
                # pop(-3) will pop the last 3rd element from the array
                # which is the size in bytes
                t1 = str(entry).lower().replace(" " + names_as_array[idx].lower(), "").split(" ")
                size = int(t1.pop(-3))
                response.append({"type": "file", "name": abs_path, "simple_name": file_name, "file_size": size})

        return response

    def decode(self, path: str) -> str:
        """decodes a given path to match HDFS structure"""
        if not path:
            return None

        for entry in self.lan_config:
            root = entry['root']
            actual = entry['actual_path']
            pos = path.lower().find(root.lower())
            #            self.log.debug(f"checking {path} against {root}; found {pos}")
            if pos >= 0:
                # if the path begins with a specific /LANxx name, then we can replace it with its real value for
                # internal use
                self.log.debug(f"decoded {path} from {root} to {actual}")
                path = path.lower().replace(root.lower(), actual.lower())
                return path
        self.log.debug(f"No matches found for {path} in the dictionary")
        return path

    def encode(self, path: str) -> str:
        """encodes a given path to not reflect HDFS structure"""
        if not path:
            return None

        for entry in self.lan_config:
            root = entry['root']
            actual = entry['actual_path']
            pos = path.lower().find(actual.lower())
            #            self.log.debug(f"checking {path} against {actual}; found {pos}")
            if pos >= 0:
                # if the path begins with a specific /LANxx name, then we can replace it with its real value for
                # internal use
                self.log.debug(f"encoded {path} from {actual} to {root}")
                path = path.lower().replace(actual.lower(), root.lower())
                return path
        self.log.debug(f"No matches found for {path} in the dictionary")
        return path
