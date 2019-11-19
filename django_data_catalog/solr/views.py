from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from django_data_catalog.file_browser.hdfs_file_browser import MaprFSBrowser
from django_data_catalog.CustomLogger import CustomLogger
from django.conf import settings


class SolrPush(APIView):
    LOG = CustomLogger.logger

    def get(self, request: Request) -> Response:
        """No Need to build this just yet."""
        self.LOG.debug("Solr Push service invoked, this feature is not implemented yet")
        return Response(data=None, status=status.HTTP_501_NOT_IMPLEMENTED)
