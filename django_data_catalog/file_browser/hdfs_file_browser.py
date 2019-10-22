import pyarrow as pa
import pyarrow.parquet as pq
import json
from pathlib import Path
from django_data_catalog.CustomLogger import CustomLogger
from django_data_catalog.solr.solr_writer import Solr
from pathlib import Path
import re

class MaprFSBrowser:
    log = CustomLogger().logger
    fsm = [
        {"root":"/LAN34","actual_path":"/edl/auto"},
        {"root":"/LAN33","actual_path":"/edl/cards"},
        {"root":"/tmp","actual_path":"/tmp"}
    ]

    def list_files(self, root_dir, mapr_user=None, mapr_password=None, host="localhost"):
        """list all folders and files in 'root_dir' folder"""
        self.log.debug(f"listing contents of folder {root_dir}")
        current_dir = root_dir
        fs = None
        data_children=[]
        if current_dir.strip() == '/':
            CustomLogger.logger.debug (f"root folder ({current_dir}) chosen to list files under, returning pre-set root list (LAN numbers)")
            for entry in self.fsm:
                # name and full path will be same for folders like lanXX
                data_children.append({'name':entry['root']+"/",'last_modified':0,'last_accessed':0,'full_path':entry['root']+"/",'size':0})
            data={'folder':current_dir,'children':data_children}
            json_str=json.dumps(data)
            self.log.debug(f"returning {json_str} for request to list {current_dir}")
            return data

        # by now, we must have the folder name, we need to decode the LAN34 and stuff into its real representation using the fsm dictionary
        current_dir=self.decode(current_dir)

        try:
            fs = self.connect(host, mapr_user)
            if( not fs.exists(current_dir)):
                self.log.debug ("File doesn't exist")
                return None
            data = self.list_content_in_folder(fs, current_dir,mapr_user, mapr_password, host)
            self.log.debug(f"got data {json.dumps(data)}")                
        except Exception:
            self.log.debug ("unable to connect to host")
            raise

        return data

# ==================

    def list_content_in_folder(self, fs, folder,mapr_user,mapr_password, host):
        """lists contents of a folder """
        files=[]
        for entry_in_current_dir in fs.ls(folder):
            document={}
            if len(entry_in_current_dir.strip()) > 0:
                path = Path(entry_in_current_dir)
                self.log.debug(f"found file {entry_in_current_dir}")
                info=fs.info(f"{path}")
                encoded_file_path = self.encode(entry_in_current_dir)
                if(not fs.isdir(entry_in_current_dir)):
                    document = {    
                        'full_path':f'{encoded_file_path}',
                        'name': Path(encoded_file_path).name,
                        'last_modified': info['last_modified'],
                        'last_accessed' : info['last_accessed'], 
                        'size':info['size'],
                        'schema':self.get_file_info(entry_in_current_dir,mapr_user,mapr_password,host)
                        }
                else:
                    document = {    
                        'full_path':f'{encoded_file_path}/',
                        'name': Path(encoded_file_path).name+"/",
                        'last_modified': 0,
                        'last_accessed' : 0, 
                        'size':0,
                        'schema':None
                        }
            files.append(document)

        if (not folder.endswith("/")):
            folder = folder + "/"
        dir_content = {
            "folder":self.encode(folder),
            "children": files
        }
        return dir_content

# ==================

    def decode(self, path):
        if path == None:
            return None
        
        for entry in self.fsm:
            root = entry['root']
            actual = entry['actual_path']
            pos = path.lower().find(root.lower()) #case insensitive search
            self.log.debug (f"checking {path} against {root}; found {pos}")
            # this check is mainly to help with debugging.
            # ideally we should just run the re.compile(xx,yy).sub(aa,bb) command directly
            if pos >= 0:
                # if the path begins with a specific /LANxx name, then we can replace it with its real value for internal use
                self.log.debug(f"decoded {path} from {root} to {actual}")
                path = re.compile(root,re.IGNORECASE).sub(actual, path)
                self.log.debug(f"path after replacement {path}")
                return path
        self.log.debug (f"No matches found for {path} in the dictionary")
        return path

# ==================

    def encode(self, path):
        if path == None:
            return None
        
        for entry in self.fsm:
            root = entry['root']
            actual = entry['actual_path']
            pos = path.find(actual)
            self.log.debug (f"checking {path} against {actual}; found {pos}")
            if pos >= 0:
                # if the path begins with a specific /LANxx name, then we can replace it with its real value for internal use
                self.log.debug(f"encoded {path} from {actual} to {root}")
                path = re.compile(actual,re.IGNORECASE).sub(root, path)
                self.log.debug(f"path after replacement {path}")
                return path
        self.log.debug (f"No matches found for {path} in the dictionary")
        return path

# ==================

    def get_file_info(self, file_name, mapr_user=None, mapr_password=None, host="localhost"):
        """details file info for a given file, this call requires the full path of the file"""
        fs = None
        result = []

        file_name = self.decode(file_name)
        self.log.debug(f"Looking to get details for file {file_name}")
        if not file_name.endswith('parquet'):
            self.log.debug ("not a parquet file, cannot work with this for now")
            raise Exception(f"can only work with parquet file, this {file_name} is not a parquet file")

        try:
            self.log.debug ("connecting to MapR-FS")
            fs = self.connect(host, mapr_user)
        except Exception:
            self.log.debug ("unable to connect to host")
            raise
        self.log.debug(f"checking if file '{file_name}' exists")
        if not fs.exists(file_name):
            self.log.debug ("file not found")
            raise Exception(f"File '{file_name}' not found")


        self.log.debug(f"preparing to read schema offile '{file_name}'")
        with fs.open(file_name) as file:
            schema=pq.read_schema(file)
            names = schema.names
            self.log.debug(f"found {len(names)} entries in schema for file '{file_name}'")
            for name in names:
                result.append({name:str(schema.field_by_name(name).type)})
        return result


    def connect(self, host, user):
        #configure_server(host,user)
        self.log.debug (f"connect: trying to connect to [{user}@{host}]")
        fs = pa.hdfs.connect(host=host, user=user)
        return fs
