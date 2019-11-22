from django.shortcuts import render

# Create your views here.
import os
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import base_user
from rest_framework.response import Response
from rest_framework.request import Request
from django_data_catalog.file_browser.hdfs_file_browser import MaprFSBrowser
from django_data_catalog.CustomLogger import CustomLogger
from django_data_catalog.file_browser.local_file_browser import LocalFSBrowser
from .forms import StorageFileForm

browser = MaprFSBrowser()


class LocalFileFromCommandLine(APIView):
    log = CustomLogger().logger

    def get(self, request: Request):
        """ Prints files/folders from local disk """
        user = request.user
        folder = request.GET.get("folder", '/')
        self.log.debug(f"printing files/folders from root {folder}")
        fs_browser = LocalFSBrowser()
        content = fs_browser.list_using_tree(folder)
        return Response(data=content)


class LocalFileFromService(APIView):
    log = CustomLogger().logger

    def get(self, request: Request) -> Response:
        """ Prints files/folders from local disk """
        folder = request.GET.get("folder", '/')
        self.log.debug(f"printing files/folders from root {folder}")
        fs_browser = LocalFSBrowser()
        content = fs_browser.list_folders(folder)
        return Response(data=content)

    def put(self, request: Request) -> Response:
        """ writes files to local disk (or SAN storage) """
        folder = request.GET.get("folder", '/')
        file_form = StorageFileForm(request.POST, request.FILES)
        if not file_form.is_valid():
            # Something is not right.
            return Response(data={"error": "please review the request object; file not saved"},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

        file_ref = request.FILES['file_ref']
        file_location = request.data['file_location']
        file_name = request.data['file_name']
        try:
            LocalFSBrowser().store_file(file=file_ref, dir_name=file_location, file_name=file_name)
        except IOError as e:
            return Response(data={"error":str(e)},status=status.HTTP_304_NOT_MODIFIED)

        self.log.debug(f"printing files/folders from root {folder}")
        fs_browser = LocalFSBrowser()
        content = fs_browser.list_folders(folder)
        return Response(data=content)


class LocalFilesystemContentDownloadView(APIView):
    log = CustomLogger().logger

    def get(self, request):
        """ downloads a file from disk """
        file_path = request.query_params.get("file_path")
        if not file_path:
            # no file_path supplied.
            resp = "`file_path` is a mandatory field and cannot be empty"
            self.log.debug(resp)
            return Response(data=resp, status=status.HTTP_400_BAD_REQUEST)
        self.log.debug(f"looking to download file {file_path}")

        if not os.path.exists(file_path):
            resp = f"no file was found at {file_path}"
            self.log.debug(resp)
            return Response(data=resp, status=status.HTTP_404_NOT_FOUND)

        if not os.path.isfile(file_path):
            resp = f"this {file_path} is not a file"
            self.log.debug(resp)
            return Response(data=resp, status=status.HTTP_406_NOT_ACCEPTABLE)

        # file exists
        handle = open(file_path, 'rb')
        response = Response(handle, content_type="application/file")
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
        return response


class ListHDFSFiles(APIView):
    log = CustomLogger().logger

    def get(self, request, mapr_user="mapr", mapr_password=None):
        #        host = request.GET.__getitem__("host")
        folder = request.GET.get("folder", '/')
        host = request.GET.get("host", 'localhost')
        #        mapr_user = request.GET.__getitem__("user")
        #        mapr_password = request.GET.__getitem__("password") # need to unhash this value before using
        mapr_password = None  # don't want to use the unhashed password, so ignoring the implementation for now
        content = {}
        try:
            content = browser.list_files(folder, mapr_user, mapr_password, host)
        except Exception:
            self.log.debug(f"Found exception while listing files from folder {folder}")
            raise
        return Response(content)


class GetHDFSFileInfo(APIView):
    log = CustomLogger().logger

    def get(self, request, mapr_user="mapr", mapr_password=None):
        file_name = request.GET.get("file_name", None)
        host = request.GET.get("host", 'localhost')
        mapr_password = None  # dont want to use the unhashed password, so ignoring the implementation for now
        content = {}
        if not file_name:
            content = {"error": "please pass 'file_name' parameter in the URL to proceed"}
        else:
            try:
                content = browser.get_file_info(file_name, mapr_user, mapr_password, host)
            except Exception:
                self.log.debug(f"Found exception while getting file info for file {file_name}")
                content = {"error": f"File '{file_name}' not found"}

        return Response(content)
