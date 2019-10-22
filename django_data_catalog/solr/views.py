from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django_data_catalog.file_browser.hdfs_file_browser import MaprFSBrowser
from django_data_catalog.CustomLogger import CustomLogger
from django.conf import settings
from django_data_catalog.solr.populate_catalog import PopulateJob


class SolrJob(APIView):
    def get(self, request):
        job=PopulateJob()
        job.do_populate(host=settings.MAPR_HOST)
        return Response({"Job":"Done"})


        

