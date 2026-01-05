from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.apps import apps
from django.db.models import Max
from .models import Tblproject, Tbluser, Tblprojectnotes, Tblprojectdocument, Tlkdocuments, Tblprojectplatforminfo
from .forms import ProjectForm, ProjectNotesForm, ProjectDocumentsForm, ProjectPlatformInfoForm
import pandas as pd
from django.utils import timezone
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

def projects(request):
    query = request.GET.get("q")

    filter_query = {}
    if query is not None and query != '':
        filter_query['projectname__icontains'] = query
        filter_query['projectnumber__icontains'] = query

    projects = Tblproject.objects.filter(
            Q(**filter_query, _connector=Q.OR)
            , validto__isnull=True
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

    return render(request, 'Prism/projects.html', {'projects':projects})


def project(request, projectnumber):
    if request.method == "POST":
        if 'project-pid' in request.POST:
            project_form = ProjectForm(request.POST, prefix='project')
            if project_form.is_valid():
                pID = project_form.cleaned_data['pid']
                insert = Tblproject(
                    projectnumber = projectnumber
                    ,projectname = project_form.cleaned_data['projectname']
                    ,portfolionumber = project_form.cleaned_data['portfolionumber']
                    ,stage = project_form.cleaned_data['stage_id']
                    ,classification = project_form.cleaned_data['classification_id']
                    ,datrag = project_form.cleaned_data['datrag']
                    ,projectedstartdate = project_form.cleaned_data['projectedstartdate']
                    ,projectedenddate = project_form.cleaned_data['projectedenddate']
                    ,startdate = project_form.cleaned_data['startdate']
                    ,enddate = project_form.cleaned_data['enddate']
                    ,pi = project_form.cleaned_data['pi'].usernumber
                    ,leadapplicant = project_form.cleaned_data['leadapplicant'].usernumber
                    ,faculty = project_form.cleaned_data['faculty_id']
                    ,lida = project_form.cleaned_data['lida']
                    ,internship = project_form.cleaned_data['internship']
                    ,dspt = project_form.cleaned_data['dspt']
                    ,iso27001 = project_form.cleaned_data['iso27001']
                    ,laser = project_form.cleaned_data['laser']
                    ,irc = project_form.cleaned_data['irc']
                    ,seed = project_form.cleaned_data['seed']
                    ,validfrom = timezone.now()
                    ,validto = None
                    ,createdby = request.user
                )
                
                # Fetch existing project record
                existing_project = Tblproject.objects.filter(
                    validto__isnull=True
                    , projectnumber=projectnumber
                ).values(
                ).get() 

                # Only save record if fields have changed
                if recordchanged(existing_record=existing_project, form_set=insert):
                    insert.save(force_insert=True)

                    delete = Tblproject(
                        pid = pID
                        ,validto = timezone.now()
                    )
                    delete.save(update_fields=["validto"])
                
                    messages.success(request, 'Project updated successfully.')
                return HttpResponseRedirect(f"/project/{projectnumber}")
        
        elif 'p_note-pnote' in request.POST:
            p_notes_form = ProjectNotesForm(request.POST, prefix='p_note')
            if p_notes_form.is_valid():
                insert_note = Tblprojectnotes(
                    projectnumber = projectnumber
                    ,pnote = p_notes_form.cleaned_data['pnote']
                    ,created = timezone.now()
                    ,createdby = request.user
                )
                insert_note.save(force_insert=True)
                messages.success(request, 'Project note added successfully.')
                return HttpResponseRedirect(f"/project/{projectnumber}")
            
        elif 'p_platform-platforminfoid' in request.POST:
            p_platform_info_form = ProjectPlatformInfoForm(request.POST, prefix='p_platform')
            if p_platform_info_form.is_valid():
                insert_platform_info = Tblprojectplatforminfo(
                    projectnumber = projectnumber
                    ,platforminfoid = p_platform_info_form.cleaned_data['platforminfoid']
                    ,projectplatforminfo = p_platform_info_form.cleaned_data['projectplatforminfo']
                    ,validfrom = timezone.now()
                    ,validto = None
                    ,createdby = request.user
                )
                insert_platform_info.save(force_insert=True)
                messages.success(request, 'Project platform info added successfully.')
                return HttpResponseRedirect(f"/project/{projectnumber}")
    
    if request.method == 'GET':

        project = Tblproject.objects.filter(
            validto__isnull=True
            , projectnumber=projectnumber
        ).values(
        ).get()         # get() with no arguments will raise an exception if the queryset doesn't contain exactly one item

        query = request.GET.get("search_notes")
        filter_query = {}
        if query is not None and query != '':
            filter_query['pnote__icontains'] = query
        
        project_notes = Tblprojectnotes.objects.filter(
            Q(**filter_query, _connector=Q.OR)
            , projectnumber=projectnumber
        ).values(
        ).order_by("-created")

        project_docs = Tblprojectdocument.objects.filter(
            validto__isnull=True
            , projectnumber=projectnumber
        ).values(            
        ).order_by("documenttype", "versionnumber")

        project_platform_info = Tblprojectplatforminfo.objects.filter(
            validto__isnull=True
            , projectnumber=projectnumber
        ).values("projectplatforminfoid", "platforminfoid__platforminfodescription", "projectplatforminfo"
        ).order_by("platforminfoid", "projectplatforminfo")

        # Important that these top level key names match the values of [DocumentDescription] stored in the database table [tlkDocuments]
        p_docs={
            "Project Proposal":{'url':'proposal', 'status':''}
            ,"Data Management Plan":{'url':'dmp', 'status':''}
            ,"Risk Assessment":{'url':'ra', 'status':''}
        }
        for doc in p_docs:
            if project_docs.filter(documenttype__documentdescription=doc
                                , accepted__isnull=False).exists():
                p_docs[doc]["status"] = "accepted"
            elif project_docs.filter(documenttype__documentdescription=doc
                                , accepted__isnull=True).exists():
                p_docs[doc]["status"] = "present"
            else: 
                p_docs[doc]["status"] = "absent"

        paginator = Paginator(project_notes, 5)  # Show 5 posts per page
        page_number = request.GET.get('page')
        try:
            page_obj = paginator.get_page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        project_form = ProjectForm(initial=project, prefix='project')
        p_notes_form = ProjectNotesForm(prefix='p_note')
        p_platform_info_form = ProjectPlatformInfoForm(prefix='p_platform')

        return render(request, 'Prism/project.html', {'project':project
                                                , 'form':project_form
                                                , 'new_note': p_notes_form
                                                , 'notes':page_obj
                                                , 'p_docs': p_docs
                                                , 'platforminfo': project_platform_info
                                                , 'platform_form': p_platform_info_form})

def projectcreate(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():

            # Get latest ProjectNumber from database model and iterate up by one for new ProjectNumber
            max_projectnumber = Tblproject.objects.filter(
                validto__isnull=True
                ,projectnumber__startswith='P'
            ).aggregate(Max("projectnumber"))
            new_projectnumber = 'P' + str('0000' + str(int(max_projectnumber['projectnumber__max'][-4:]) +1))[-4:]
            
            insert = Tblproject(
                projectnumber = new_projectnumber
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
                ,validfrom = timezone.now()
                ,validto = None
                ,createdby = request.user
            )
            insert.save(force_insert=True)

            return HttpResponseRedirect(f"/project/{new_projectnumber}")
        else:
            return render(request, 'Prism/project.html', {'form':form})   

    if request.method == 'GET':
        form = ProjectForm()
        return render(request, 'Prism/project.html', {'form':form})
    
def recordchanged(existing_record, form_set):
    # Compare existing record to form values
    record_changed = False
    for field in existing_record:
        if form_set._meta.get_field(field).primary_key or field == 'validfrom' or field == 'validto' or field == 'createdby':
            record_changed = record_changed
        elif existing_record[field] != getattr(form_set, field):
            record_changed = True
    return record_changed

def projectdocs(request, projectnumber, doctype=None):
    if request.method == "POST":
        
        project_docs_form=ProjectDocumentsForm(request.POST)
        if project_docs_form.is_valid():
            
            # Get latest VersionNumber from database model and iterate up by one for new VersionNumber
            max_versionnumber = Tblprojectdocument.objects.filter(
                validto__isnull=True
                ,projectnumber=projectnumber
                ,documenttype=project_docs_form.cleaned_data['documenttype']
            ).aggregate(Max("versionnumber"))
            if max_versionnumber['versionnumber__max'] is not None:
                new_versionnumber = int(max_versionnumber['versionnumber__max']) +1
            else:
                new_versionnumber = 1
            
            insert = Tblprojectdocument(
                projectnumber=projectnumber
                , documenttype=project_docs_form.cleaned_data['documenttype']
                , versionnumber=new_versionnumber
                , submitted=project_docs_form.cleaned_data['submitted']
                , accepted=project_docs_form.cleaned_data['accepted']
                , validfrom=timezone.now()
                , validto=None
                , createdby=request.user
                )
            insert.save(force_insert=True)

            if doctype:
                return HttpResponseRedirect(f"/project/{projectnumber}/docs/{doctype}")
            else:
                return HttpResponseRedirect(f"/project/{projectnumber}/docs")

    if request.method == "GET":
        filter_query = {}
        # Important that these values match the values of [DocumentDescription] stored in the database table [tlkDocuments]
        doctype_dict = {None:None
                        , 'proposal': 'Project Proposal'
                        , 'dmp': 'Data Management Plan'
                        , 'ra': 'Risk Assessment'}
        if doctype is not None:
            filter_query['documenttype__documentdescription'] = doctype_dict[doctype]

        project_docs = Tblprojectdocument.objects.filter(
                Q(**filter_query, _connector=Q.OR)
                , validto__isnull=True
                , projectnumber=projectnumber
            ).values(
                'pdid'
                ,'projectnumber'
                ,'documenttype__documentdescription'
                ,'versionnumber'
                ,'submitted'
                ,'accepted'
            ).order_by("documenttype", "versionnumber")

        # Initialise documenttype input if looking at single doctype
        if doctype is not None:
            doc_id = Tlkdocuments.objects.filter(
                validto__isnull=True
                ,documentdescription=doctype_dict[doctype]
            ).values(
                'documentid'
            ).get()
            project_docs_form=ProjectDocumentsForm(initial={'documenttype':doc_id['documentid']})
        else:
            project_docs_form=ProjectDocumentsForm()

        return render(request, 'Prism/docs.html', {'project_docs':project_docs
                                                   , 'project_docs_form': project_docs_form
                                                   , 'projectnumber':projectnumber
                                                   , 'doctype':doctype_dict[doctype]
                                                   , 'doctypeurl':doctype})
    
def projectdocs_acceptwithdraw(request, projectnumber, doctype, action, pdid):
    update_record=Tblprojectdocument.objects.filter(
        pdid=pdid
        , projectnumber=projectnumber
    ).values()

    if action == 'accept':
        update_record.update(accepted = timezone.now())
    elif action == 'withdraw':
        update_record.update(accepted = None)
    
    if doctype and doctype != 'None':
        return HttpResponseRedirect(f"/project/{projectnumber}/docs/{doctype}")
    else:
        return HttpResponseRedirect(f"/project/{projectnumber}/docs")


def projectplatforminfo_remove(request, projectnumber, projectplatforminfoid):
    update_record=Tblprojectplatforminfo.objects.filter(
        projectplatforminfoid=projectplatforminfoid
        , projectnumber=projectnumber
    ).values()
    update_record.update(validto = timezone.now())
    
    return HttpResponseRedirect(f"/project/{projectnumber}")