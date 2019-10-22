from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django_data_catalog.file_browser.hdfs_file_browser import MaprFSBrowser
from django_data_catalog.CustomLogger import CustomLogger
browser = MaprFSBrowser()


class ListFiles(APIView):
    log = CustomLogger().logger
    def get(self, request, mapr_user="mapr", mapr_password=None):
#        host = request.GET.__getitem__("host")
        folder = request.GET.get("folder",'/')
        host = request.GET.get("host", 'localhost')
#        mapr_user = request.GET.__getitem__("user")
#        mapr_password = request.GET.__getitem__("password") # need to unhash this value before using
        mapr_password = None #dont want to use the unhashed password, so ignoring the implementation for now
        content = {}
        try:
            content = browser.list_files(folder,mapr_user, mapr_password, host)
        except Exception:
            self.log.debug (f"Found exception while listing files from folder {folder}")
            raise
        return Response(content)


class GetFileInfo(APIView):
    log = CustomLogger().logger
    def get(self, request,mapr_user="mapr",mapr_password=None):
        file_name = request.GET.get("file_name", None)
        host = request.GET.get("host", 'localhost')
        mapr_password = None #dont want to use the unhashed password, so ignoring the implementation for now
        content={}
        if file_name == None:
            content = {"error":"please pass 'file_name' parameter in the URL to proceed"}
        else:
            try:
                content = browser.get_file_info(file_name, mapr_user, mapr_password, host)
            except Exception:
                self.log.debug (f"Found exception while getting file info for file {file_name}")
                content={"error":f"File '{file_name}' not found"}

        return Response(content)

