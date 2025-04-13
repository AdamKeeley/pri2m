from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.apps import apps
from django.db.models import Value
from django.db.models.functions import Concat
from django.urls import reverse
from .models import Tblproject
from .forms import ProjectForm
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
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            pID = form.cleaned_data['pid']

            insert = Tblproject(
                projectnumber = projectnumber
                ,projectname = form.cleaned_data['projectname']
                ,portfolionumber = form.cleaned_data['portfolionumber']
                ,stage = form.cleaned_data['stage']
                ,classification = form.cleaned_data['classification']
                ,datrag = form.cleaned_data['datrag']
                ,projectedstartdate = form.cleaned_data['projectedstartdate']
                ,projectedenddate = form.cleaned_data['projectedenddate']
                ,startdate = form.cleaned_data['startdate']
                ,enddate = form.cleaned_data['enddate']
                ,pi = form.cleaned_data['pi']
                ,leadapplicant = form.cleaned_data['leadapplicant']
                ,faculty = form.cleaned_data['faculty']
                ,lida = form.cleaned_data['lida']
                ,internship = form.cleaned_data['internship']
                ,dspt = form.cleaned_data['dspt']
                ,iso27001 = form.cleaned_data['iso27001']
                ,laser = form.cleaned_data['laser']
                ,irc = form.cleaned_data['irc']
                ,seed = form.cleaned_data['seed']
                ,validfrom = form.cleaned_data['validfrom']
                ,validto = form.cleaned_data['validto']
                ,createdby = request.user
            )
            insert.save(force_insert=True)

            delete = Tblproject(
                pid = pID
                ,validto = datetime.now()
            )
            delete.save(update_fields=["validto"])

            return HttpResponseRedirect(f"/project/{projectnumber}")
        else:
            return render(request, 'project.html', {'form':form})
    
    if request.method == 'GET':
        project = Tblproject.objects.filter(
            validto__isnull=True
            , projectnumber=projectnumber
        ).values(
        ).annotate(
            pi_fullname = Concat('pi__firstname', Value(' '), 'pi__lastname')
            ,leadapplicant_fullname = Concat('leadapplicant__firstname', Value(' '), 'leadapplicant__lastname')
        ).get()         # get() with no arguments will raise an exception if the queryset doesn't contain exactly one item
        form = ProjectForm(initial=project)
        return render(request, 'project.html', {'project':project
                                                , 'form':form})

 