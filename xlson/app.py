""" Importing required strings """
from typing import Any

from django import forms
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django_micro import configure, run

DEBUG = True
configure(locals())


class UploadFileForm(forms.Form):
    """ models for uploaded file """

    files = forms.FileField()


def upload_file(request: HttpRequest) -> HttpResponse:
    """ handle all uploads """
    if request.method == "POST":
        # get the uploaded file through the uploadFileform model
        form: Any = UploadFileForm(request.POST, request.FILES)

        # get the file extension
        ext: str = request.FILES.get("form").name.split(".")[-1]

        # validate file is xlsx or xls
        if ext not in ("xlsx", "xls"):
            render(request, "upload.html", status=400)
        render(request, "upload.html", {"form": form})
    else:
        form = UploadFileForm()
    return render(request, "upload.html", {"form": form})


APPLICATION = run()
