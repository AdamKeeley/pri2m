from django.shortcuts import render
from django.apps import apps
import pyodbc
from .models import Tblproject


def projects(request):
    projects = Tblproject.objects.values("pid", "projectnumber", "projectname", "stage", "pi", "faculty")
    return render(request, 'projects.html', {'projects':projects})
