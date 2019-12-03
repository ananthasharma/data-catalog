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
from file_browser import views as file_browser_views

urlpatterns = [
    path("hdfs/browse/", file_browser_views.ListHDFSFiles.as_view()),
    path("local/browse/", file_browser_views.LocalFileBrowserFromService.as_view()),
    path("local/upload/", file_browser_views.LocalFileUploaderFromService.as_view()),
    path("local/download/", file_browser_views.LocalFileDownloaderFromService.as_view()),
]

# please copy and paste this module into any existing Django project,
# (some simple setting changes should integrate the solution)
