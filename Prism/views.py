from django.shortcuts import render
from django.apps import apps
from django.db.models import Value
from django.db.models.functions import Concat
from .models import Tblproject


def projects(request):
    projects = Tblproject.objects.filter(
            validto__isnull=True
        ).values(
            "pid"
            , "projectnumber"
            , "projectname"
            , "stage__pstagedescription"
            , "faculty__facultydescription"
        ).annotate(
            pi_fullname = Concat('pi__firstname', Value(' '), 'pi__lastname')
        ).order_by("projectnumber")
    return render(request, 'projects.html', {'projects':projects})
