""" Importing required strings """
import os

from django import forms
from django.views.generic.edit import FormView
from django_micro import configure, run

DEBUG = True
configure(locals())


CONTENT_TYPES = [".xlsx", ".xls"]
MAX_UPLOAD_SIZE = 10485760


class UploadFile(forms.Form):
    """field in the upload form"""

    files = forms.FileField()

    def clean_files(self) -> str:
        """clean data recieved from the upload form """
        files = self.cleaned_data.get("files")
        ext = os.path.splitext(files.name)[-1]
        file_size = files.size
        if ext in CONTENT_TYPES:
            if file_size >= MAX_UPLOAD_SIZE:
                raise Exception("file too large")
        else:
            raise Exception("wrong file type")
        return "uploaded"


class UploadView(FormView):  # pylint: disable=too-many-ancestors
    """ upload view """

    template_name = "upload.html"
    form_class = UploadFile
    success_url = "/thanks/"


APPLICATION = run()
