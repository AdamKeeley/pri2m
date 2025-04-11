from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.apps import apps
from django.db.models import Value
from django.db.models.functions import Concat
from django.urls import reverse
from .models import Tblproject
from .forms import ProjectForm
from .helper import delete_record


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
        ).annotate(
            pi_fullname = Concat('pi__firstname', Value(' '), 'pi__lastname')
            ,leadapplicant_fullname = Concat('leadapplicant__firstname', Value(' '), 'leadapplicant__lastname')
        ).get()         # get() with no arguments will raise an exception if the queryset doesn't contain exactly one item
        form = ProjectForm(initial=project)
        return render(request, 'project.html', {'project':project
                                                , 'form':form})
    
def projectdelete(request, projectnumber):
    project = Tblproject.objects.filter(
            validto__isnull=True
            , projectnumber = projectnumber
        ).values(
            "pid"
        ).get()
    tbl_name = "dbo.tblProject"
    pk_field = "pID"
    pk_value = project["pid"]
    delete_record(tbl_name, pk_field, pk_value)
    return redirect(projects)
 