from django.shortcuts import render, HttpResponse
from django.apps import apps
from django.db.models import Value
from django.db.models.functions import Concat
from .models import Tblproject
from .forms import ProjectForm


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
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            return HttpResponse("/thanks/")
        else:
            return render(request, 'project.html', {'form':form})
    
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
        ).get()         # get() with no arguments will raise an exception if the queryset doesn't contain exactly one item
        form = ProjectForm(initial=project)
        return render(request, 'project.html', {'project':project
                                                , 'form':form})