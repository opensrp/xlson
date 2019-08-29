""" Importing required strings """
import os
from typing import Any

import pandas as pd
from django import forms
from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django_micro import configure, route, run

EXTENSION_TYPES = [".xlsx", ".xls"]
MAX_UPLOAD_SIZE = 10485760
FILETYPE_ERROR = "wrong file type"
FILESIZE_ERROR = "file too large"
SUCCESFULL_UPLOAD = "File has been uploaded"
UPLOAD_FILES = "files"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT = os.path.join(BASE_DIR, "xlson/uploaded_files/")
MEDIA_URL = "upload_-files/"


DEBUG = True
configure(locals())


class UploadFile(forms.Form):
    """field in the upload form"""

    files = forms.FileField()

    def clean_files(self) -> Any:
        """clean data recieved from the upload form """
        files = self.cleaned_data.get(settings.UPLOAD_FILES)
        ext = os.path.splitext(files.name)[-1]
        file_size = files.size
        if ext in settings.EXTENSION_TYPES:
            if file_size >= settings.MAX_UPLOAD_SIZE:
                raise forms.ValidationError(settings.FILESIZE_ERROR)
        else:
            raise forms.ValidationError(settings.FILETYPE_ERROR)
        return files


@route("", name="UploadFile")  # pylint: disable=too-many-ancestors
class UploadView(FormView):  # pylint: disable=too-many-ancestors
    """ upload view """

    template_name = "upload.html"
    form_class = UploadFile
    success_url = reverse_lazy("UploadFile")

    def form_valid(self, form: Any) -> HttpResponse:
        """ handle post requests """
        output = self.handle_uploaded_file(form.files["files"])
        print(output)
        return HttpResponse("file succesfully processed")

    def handle_uploaded_file(self, files: Any) -> Any:  # pylint: disable=R0201
        """ Read the uploaded xls file"""
        import ipdb

        ipdb.set_trace()
        new_file = os.path.join(settings.MEDIA_ROOT, files.name)
        with open(new_file, "wb+") as destination:
            for chunk in files.chunks():
                destination.write(chunk)
        workbook = pd.read_excel(open(new_file, "rb"))
        return workbook


APPLICATION = run()
