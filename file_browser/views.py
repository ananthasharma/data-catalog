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


class LocalFileFromService(APIView):
    log = CustomLogger().logger

    def get(self, request: Request) -> Response:
        """ Prints files/folders from local disk """
        folder = request.GET.get("folder", '/')
        default_folder: str = settings.BASE_FOLDER_FOR_FILE_BROWSER
        if not default_folder.endswith("/"):
            default_folder = default_folder + "/"
        folder: str = request.GET.get("folder", default_folder)
        if not folder.lower().startswith(default_folder.lower()):
            # this is a sub directory
            folder = default_folder + folder

        #        if folder.index("..") > 0:
        # the user is trying to get to a parent folder
        #           folder = default_folder
        #          self.log.warn(f"user is trying to list content outside configured boundaries")

        self.log.debug(f"printing files/folders from root {folder}; base_folder : {default_folder}")
        fs_browser = LocalFSBrowser()
        folder = folder.replace("//", "/")
        try:
            content = fs_browser.list_folders(folder)
        except ValueError as err:
            return Response(data=str(err), status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(data=content)

    def delete(self, request: Request) -> Response:
        """Deletes a given file (not folder)"""
        file_to_delete = request.GET.get("file_to_delete", None)
        if not file_to_delete:
            # nothing was sent for deletion
            self.log.error("No file sent for delete operation")
            return Response(data={"error": "No file supplied for delete; use `file_to_delete` property as query_param "
                                           "to specify a file"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            LocalFSBrowser().remove_file(file_to_delete)
            self.log.info(f"deleted file {file_to_delete}")
        except ValueError as err:
            return Response(data={"error": str(err)}, status=status.HTTP_304_NOT_MODIFIED)

        return Response(data={"status": "success"}, status=status.HTTP_204_NO_CONTENT)

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
            return Response(data={"error": str(e)}, status=status.HTTP_304_NOT_MODIFIED)

        self.log.debug(f"printing files/folders from root {file_location}")
        fs_browser = LocalFSBrowser()
        content = fs_browser.list_folders(file_location)
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
    file_browser = HDFSCommandLineFileBrowser()

    def get(self, request):
        folder = request.GET.get("folder_path", '/')
        self.log.info(f"got request to list contents of {folder}")
        content = {}
        try:
            content = self.file_browser.listFiles(folder)
            self.log.info(f"success; returning {len(content)} items as dir listing of {folder}")
        except Exception:
            self.log.debug(f"Found exception while listing contents of {folder}")
            raise
        return Response(content)

