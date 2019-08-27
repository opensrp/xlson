""" Importing required strings """
import os
from typing import Any

from django import forms
from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django_micro import configure, route, run

CONTENT_TYPES = [".xlsx", ".xls"]
MAX_UPLOAD_SIZE = 10485760
FILETYPE_ERROR = "wrong file type"
FILESIZE_ERROR = "file too large"
SUCCESFULL_UPLOAD = "File has been uploaded"


DEBUG = True
configure(locals())


class UploadFile(forms.Form):
    """field in the upload form"""

    files = forms.FileField()

    def clean_files(self) -> Any:
        """clean data recieved from the upload form """

        files = self.cleaned_data.get("files")
        ext = os.path.splitext(files.name)[-1]
        file_size = files.size
        if ext in settings.CONTENT_TYPES:
            if file_size >= settings.MAX_UPLOAD_SIZE:
                raise Exception(settings.FILESIZE_ERROR)
        else:
            raise Exception(settings.FILETYPE_ERROR)
        return settings.SUCCESFULL_UPLOAD


@route("", name="UploadFile")  # pylint: disable=too-many-ancestors
class UploadView(FormView):  # pylint: disable=too-many-ancestors
    """ upload view """

    template_name = "upload.html"
    form_class = UploadFile
    success_url = reverse_lazy("UploadFile")


APPLICATION = run()
