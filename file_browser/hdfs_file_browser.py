from core.CustomLogger import CustomLogger
import os
from django.conf import settings


class HDFSCommandLineFileBrowser:
    log = CustomLogger.logger

    def listFiles(self, folder_path: str) -> [str]:
        """Lists files using a shell command
        approach::
        use hdfs dfs -ls <<folder path>> command to list all folders and files; call this output
        use hdfs dfs -ls -C <<folder path>> command to list only file or folder names; call this output_names
        **** it is assumed that nothing changed in the folders between these two commands running ****
        split each entry in output by line; remove matching names from output_names (as they are in the same order);
        figure out of the entry is a file or folder by checking if entries in output starts with "d"
        prepare response
        """
        self.log.debug(f"service invoked for folder :{folder_path}")

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
        for idx, entry in enumerate(listings_as_array):
            abs_path = names_as_array[idx]
            file_name = abs_path.split("/").pop()
            if str(entry).startswith("d"):
                # then names_as_array[idx] is a folder
                response.append(
                    {"type": "directory", "name": names_as_array[idx], "simple_name": file_name, "contents": []})
            else:
                # extract the last elem
                # "['drwx------   - asharma staff         64 2019-12-01 20:54 .Trash']"
                # when we replace "<blank space> file name" with blank we get
                # "['drwx------   - asharma staff         64 2019-12-01 20:54']"
                # we need to split this into an array separated by space, then we get
                # ['drwx------', '', '', '-', 'asharma', 'staff', '', '', '', '', '', '', '', '', '64', '2019-12-01', '20:54']
                # pop(-3) will pop the last 3rd element from the array
                # which is the size in bytes
                t1 = str(entry).lower().replace(" " + abs_path.lower(), "").split(" ")
                size = int(str(entry).lower().replace(" " + abs_path.lower(), "").split(" ").pop(-3))
                response.append({"type": "file", "name": abs_path, "simple_name": file_name, "file_size": size})

        return response
