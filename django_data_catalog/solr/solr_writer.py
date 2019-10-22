import pysolr
import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd
import json
from django.conf import settings
from django_data_catalog.CustomLogger import CustomLogger

class Solr:
    log = CustomLogger().logger
    solr_host = settings.solr_host_ip
    solr_port = settings.solr_port
    solr_path = settings.solr_path
    # TODO: check for leading and trailing / in solr path
    # TODO: check if host is valid ip addr
    solr_url = f"http://{solr_host}:{solr_port}/{solr_path}/"

    solr = None

    def prepare(self):
        """ checks if solr object is initialized, initializes it if needed and returns """
        if self.solr == None:
            log.debug(f'connecting to Solr at Url {solr_url}')
            self.solr = pysolr.Solr(self.solr_url, timeout=10, auth=None)


    def write(self, content):
        self.prepare()
        self.solr.add(docs=content, commit=True)
    
