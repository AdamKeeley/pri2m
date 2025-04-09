from django.shortcuts import render
from django.apps import apps
from django.db.models import Value
from django.db.models.functions import Concat
from .models import Tblproject, Tlkstage, Tlkclassification, Tlkfaculty
from datetime import datetime


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

def project(request, projectnumber):
    if request.method == 'GET':
        project = Tblproject.objects.filter(
                validto__isnull=True
                , projectnumber=projectnumber
            ).values(
                "pid"
                , "projectnumber"
                , "projectname"
                , "stage__pstagedescription"
                , "classification__classificationdescription"
                , "projectedstartdate"
                , "projectedenddate"
                , "startdate"
                , "enddate"
                , "faculty__facultydescription"
                , "lida"
                , "internship"
                , "dspt"
                , "iso27001"
                , "laser"
                , "irc"
                , "seed"
                , "validfrom"
                , "validto"
                , "createdby"
            ).annotate(
                pi_fullname = Concat('pi__firstname', Value(' '), 'pi__lastname')
                ,leadapplicant_fullname = Concat('leadapplicant__firstname', Value(' '), 'leadapplicant__lastname')
            )
        project_dict = dict(project.first())
        stages = Tlkstage.objects.all().filter(validto__isnull=True)
        classifications = Tlkclassification.objects.all().filter(validto__isnull=True)
        faculties = Tlkfaculty.objects.all().filter(validto__isnull=True)
        return render(request, 'project.html', {'project':project_dict
                                                , 'stages':stages
                                                , 'classifications':classifications
                                                , 'faculties':faculties})