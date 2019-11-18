"""django_data_catalog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django_data_catalog.file_browser import views as hdfs_file_browser_views
from django_data_catalog.file_browser import views as local_file_browser


urlpatterns = [
    path('admin/', admin.site.urls),
    path("hdfs/browse/", hdfs_file_browser_views.ListHDFSFiles.as_view()),
    path("hdfs/file_info/", hdfs_file_browser_views.GetHDFSFileInfo.as_view()),
#    path("local/list_tree/", hdfs_file_browser_views.LocalFileFromCommandLine.as_view()),
    path("local/list/", hdfs_file_browser_views.LocalFileFromService.as_view()),
    path("local/download/", hdfs_file_browser_views.LocalFilesystemContentDownloadView.as_view()),
]
