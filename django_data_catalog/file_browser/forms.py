from django import forms


class StorageFileForm(forms.Form):
    """Class representing an uploaded file"""
    file_name = forms.CharField(max_length=500)
    file_location = forms.CharField(max_length=500)
    file_ref = forms.FileField()
