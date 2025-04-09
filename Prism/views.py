from django.shortcuts import render
from django.apps import apps
from .models import Tblproject


def projects(request):
    projects = Tblproject.objects.filter(
            validto__isnull=True
        ).values(
            "pid"
            , "projectnumber"
            , "projectname"
            , "stage__pstagedescription"
            , "pi__lastname"
            , "faculty__facultydescription"
        ).order_by("projectnumber")
    return render(request, 'projects.html', {'projects':projects})
