from django_data_catalog.file_browser.hdfs_file_browser import MaprFSBrowser
from django_data_catalog.CustomLogger import CustomLogger
from django_data_catalog.solr.solr_writer import Solr
import json

class PopulateJob:
    log = CustomLogger().logger
    browser = MaprFSBrowser()
    solr = Solr()

    def do_populate(self, host):
        """ entry point into data population"""
        self.log.debug(f"Beginning Solr sync with FS")
        self.recurse_listing("/",host)

# ==========

    def recurse_listing(self, start_folder, host):
        """ recursively list all folders and files inside them"""
        folder_list = self.browser.list_files(root_dir=start_folder, host=host)
        #self.log.debug(f'got folder info for folder {start_folder} as {json.dumps(folder_list)}')
        if folder_list == None:
            # folder doesnt exist
            return
        for entry in folder_list['children']:
            if entry['name'].endswith('/'):
                self.log.debug(f"Found folder at {entry['name']}")
                # this is a folder
                full_path=start_folder+entry["name"]
                self.log.info (f'processing folder {full_path} in parent {start_folder}')
                self.recurse_listing(start_folder=full_path,host=host)
            else:
                document_for_solr = {
                    'file_name':entry['name'],
                    'file_path':entry['full_path'],
                    'schema':entry['schema']
                } 
                self.log.debug (f'writing document to solr {document_for_solr}')
                self.solr.write(document_for_solr)

