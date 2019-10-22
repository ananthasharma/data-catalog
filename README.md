# data-catalog


ensure solr is setup and running (look at settings.py and change URL, port and path)

defaults:
solr host: http://192.168.190.133 
solr port: 8983
solr core name: new_core


test:
$ curl http://localhost:8000/browse?folder=/

$ curl http://localhost:8000/solr_job

$ # test solr core content, you should see 1 entry for each file and each column in that file
