from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.apps import apps
from django.db.models import Value, F
from django.db.models.functions import Concat
from .models import Tblproject, Tbluser
from .forms import ProjectForm
from datetime import datetime
import pandas as pd


def projects(request):
    projects = Tblproject.objects.filter(
            validto__isnull=True
        ).values(
            "pid"
            , "projectnumber"
            , "projectname"
            , "stage__pstagedescription"
            , "pi"
            , "faculty__facultydescription"
        ).order_by("projectnumber")

    users = Tbluser.objects.filter(
            validto__isnull=True
            ).values()
    
    df = pd.DataFrame(users)

    for project in projects:
        if project['pi'] is not None:
            pi_index = df.index[df['usernumber'] == project['pi']].tolist()
            pi_name = f"{df.at[pi_index[0],'firstname']} {df.at[pi_index[0],'lastname']}"
            project.update(pi=pi_name)

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
                ,stage = form.cleaned_data['stage_id']
                ,classification = form.cleaned_data['classification_id']
                ,datrag = form.cleaned_data['datrag']
                ,projectedstartdate = form.cleaned_data['projectedstartdate']
                ,projectedenddate = form.cleaned_data['projectedenddate']
                ,startdate = form.cleaned_data['startdate']
                ,enddate = form.cleaned_data['enddate']
                ,pi = form.cleaned_data['pi'].usernumber
                ,leadapplicant = form.cleaned_data['leadapplicant'].usernumber
                ,faculty = form.cleaned_data['faculty_id']
                ,lida = form.cleaned_data['lida']
                ,internship = form.cleaned_data['internship']
                ,dspt = form.cleaned_data['dspt']
                ,iso27001 = form.cleaned_data['iso27001']
                ,laser = form.cleaned_data['laser']
                ,irc = form.cleaned_data['irc']
                ,seed = form.cleaned_data['seed']
                ,validfrom = datetime.now()
                ,validto = None
                ,createdby = request.user
            )
            insert.save(force_insert=True, )

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
        ).get()         # get() with no arguments will raise an exception if the queryset doesn't contain exactly one item

        form = ProjectForm(initial=project)
        return render(request, 'project.html', {'project':project
                                                , 'form':form})

 