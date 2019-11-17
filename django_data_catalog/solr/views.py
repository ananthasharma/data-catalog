from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django_data_catalog.file_browser.hdfs_file_browser import MaprFSBrowser
from django_data_catalog.CustomLogger import CustomLogger
from django.conf import settings


class SolrPush(APIView):
    def get(self, request):

