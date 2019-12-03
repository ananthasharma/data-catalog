# Create your views here.
import os
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from core.CustomLogger import CustomLogger
from .local_file_browser import LocalFSBrowser
from .hdfs_file_browser import HDFSCommandLineFileBrowser
from .forms import StorageFileForm
from django.conf import settings


class LocalFileBrowserFromService(APIView):
    log = CustomLogger().logger

    def get(self, request: Request) -> Response:
        """ Prints files/folders from local disk """
        folder = request.GET.get("path", None)
        if not folder:
            self.log.error(f"folder name not available in `path` parameter, not processing request")
            resp = {"error": f"`path` parameter in http GET is mandatory"}
            return Response(data=resp, status=status.HTTP_400_BAD_REQUEST)

        self.log.debug(f"printing files/folders from root {folder}")
        fs_browser = LocalFSBrowser()
        folder = folder.replace("//", "/")
        try:
            content = fs_browser.list_folders(folder)
        except ValueError as err:
            return Response(data=str(err), status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(data=content)


class LocalFileUploaderFromService(APIView):
    log = CustomLogger().logger

    def post(self, request: Request) -> Response:
        """ writes files to local disk (or SAN storage) """
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
            return Response(data={"error": "an error occured while uploading file; perhaps the folder contains the "
                                           "file already or we are unable to create the folder"},
                            status=status.HTTP_304_NOT_MODIFIED)

        self.log.debug(f"printing files/folders from root {file_location}")
        fs_browser = LocalFSBrowser()
        content = fs_browser.list_folders(file_location)
        return Response(data=content)


class LocalFileDownloaderFromService(APIView):
    log = CustomLogger().logger

    def get(self, request):
        """ downloads a file from disk """
        file_path = request.query_params.get("path", None)
        if not file_path:
            self.log.error(f"folder name not available in `path` parameter, not processing request")
            resp = {"error": f"`path` parameter in http GET is mandatory"}
            return Response(data=resp, status=status.HTTP_400_BAD_REQUEST)
        self.log.debug(f"looking to download file {file_path}")

        if not os.path.exists(file_path):
            resp = {"error": f"no file was found at {file_path}"}
            self.log.debug(resp)
            return Response(data=resp, status=status.HTTP_404_NOT_FOUND)

        if not os.path.isfile(file_path):
            resp = {"error": f"The path [{file_path}] is not a file"}
            self.log.debug(resp)
            return Response(data=resp, status=status.HTTP_406_NOT_ACCEPTABLE)

        # file exists
        handle = open(file_path, 'rb')
        response = Response(handle, content_type="application/file")
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
        return response


class ListHDFSFiles(APIView):
    log = CustomLogger().logger
    file_browser = HDFSCommandLineFileBrowser()

    def get(self, request):
        folder = request.GET.get("path", None)
        if not folder:
            self.log.error(f"folder name not available in `path` parameter, not processing request")
            resp = {"error": f"`path` parameter in http GET is mandatory"}
            return Response(data=resp, status=status.HTTP_400_BAD_REQUEST)

        self.log.info(f"got request to list contents of {folder}")
        content = {}
        try:
            content = self.file_browser.list_files(folder)
            self.log.info(f"success; returning {len(content)} items as dir listing of {folder}")
        except Exception:
            self.log.debug(f"Found exception while listing contents of {folder}")
            raise
        return Response(content)
