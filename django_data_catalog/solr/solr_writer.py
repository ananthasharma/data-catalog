import pysolr
import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd
import json
from django.conf import settings
from django_data_catalog.CustomLogger import CustomLogger

class Solr:
    log = CustomLogger().logger
    solr_host = settings.SOLR_HOST_IP
    solr_port = settings.SOLR_PORT
    solr_path = settings.SOLR_PATH
    # TODO: check for leading and trailing / in solr path
    # TODO: check if host is valid ip addr
    solr_url = f"http://{solr_host}:{solr_port}/solr/{solr_path}/"

    solr = None

    def prepare(self):
        """ checks if solr object is initialized, initializes it if needed and returns """
        if self.solr == None:
            self.log.debug(f'connecting to Solr at Url {self.solr_url}')
            self.solr = pysolr.Solr(self.solr_url, timeout=10, auth=None)


    def write(self, content):
        self.prepare()
        for schema_entry in content['schema']:
            column_name=list(schema_entry.keys())[0]
            value = schema_entry[column_name]
            document = {
                'file_name':content['file_name'],
                'file_path':content['file_path'],
                'column_name':column_name,
                'column_type':value,
                'id': f"{content['file_path']}#{column_name}={value}"
                }
            self.log.debug(f"Preparing to write {json.dumps(document)}")
            self.solr.add(docs=[document], commit = True, overwrite = True)
    
