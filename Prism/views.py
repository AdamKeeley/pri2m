from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.apps import apps
from django.db.models import Max, Count, OuterRef, Subquery
from .models import Tblproject, Tbluser, Tblprojectnotes, Tblprojectdocument, Tlkdocuments, Tblprojectplatforminfo \
    , Tblprojectdatallocation, Tbluserproject, Tblkristal, Tblprojectkristal, Tlkstage, Tlkfaculty, Tlkclassification \
    , Tlkuserstatus, Tblusernotes
from .forms import ProjectSearchForm, ProjectForm, ProjectNotesForm, ProjectDocumentsForm, ProjectPlatformInfoForm \
    , ProjectDatAllocationForm, UserSearchForm, UserForm, UserProjectForm, UserNotesForm
import pandas as pd
from django.utils import timezone
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from collections import namedtuple


def index(request):
    return render(request, 'Prism/index.html')

def projects(request):
    query = request.GET

    filter_query = {}
    advanced_filter_query = {}
    user_filter_query = {}
    filter_list = []

    if query is not None and query != '':
        for key in query:
            value = query.get(key)
            if value != '':
                if key == 'q':
                    filter_query['projectname__icontains'] = value
                    filter_query['projectnumber__icontains'] = value
                    filter_list.append(f"Project Number or Name contains '{value}'")
                if key == 'stage_id':
                    advanced_filter_query['stage__stageid__iexact'] = value
                    filter_list.append(f"Stage is '{Tlkstage.objects.get(stageid=value)}'")
                if key == 'classification_id':
                    advanced_filter_query['classification__classificationid__iexact'] = value
                    filter_list.append(f"Risk Class is '{Tlkclassification.objects.get(classificationid=value)}'")
                if key == 'user':
                    user_filter_query['pi__iexact'] = value
                    user_filter_query['leadapplicant__iexact'] = value
                    filter_list.append(f"PI or Lead Applicant is '{Tbluser.objects.get(usernumber=value, validto__isnull=True)}'")
                if key == 'faculty_id':
                    advanced_filter_query['faculty__facultyid__iexact'] = value
                    filter_list.append(f"Faculty is '{Tlkfaculty.objects.get(facultyid=value)}'")
                if key == 'laser':
                    advanced_filter_query['laser__iexact'] = True
                    filter_list.append(f"LASER = {True}")
                if key == 'internship':
                    advanced_filter_query['internship__iexact'] = True
                    filter_list.append(f"DSDP = {True}")

    projects = Tblproject.objects.filter(
            Q(**filter_query, _connector=Q.OR)
            , Q(**advanced_filter_query, _connector=Q.AND)
            , Q(**user_filter_query, _connector=Q.OR)
            , validto__isnull=True
        ).values(
            "pid"
            , "projectnumber"
            , "projectname"
            , "laser"
            , "internship"
            , "stage__pstagedescription"
            , "classification__classificationdescription"
            , "pi"
            , "leadapplicant"
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
        if project['leadapplicant'] is not None:
            leadapplicant_index = df.index[df['usernumber'] == project['leadapplicant']].tolist()
            leadapplicant_name = f"{df.at[leadapplicant_index[0],'firstname']} {df.at[leadapplicant_index[0],'lastname']}"
            project.update(leadapplicant=leadapplicant_name)

    filter_string = ", ".join(filter_list)
    project_search_form = ProjectSearchForm()

    return render(request, 'Prism/projects.html', {'projects': projects
                                                   ,'project_form': project_search_form
                                                   ,'searchterms': filter_string})

def project(request, projectnumber):
    # Build forms
    
    ## PROJECT ##
    project = Tblproject.objects.filter(
        validto__isnull=True
        , projectnumber=projectnumber
    ).values(
    ).get()         # get() with no arguments will raise an exception if the queryset doesn't contain exactly one item

    ## PROJECT DOCS ##
    project_docs = Tblprojectdocument.objects.filter(
        validto__isnull=True
        , projectnumber=projectnumber
    ).values(            
    ).order_by("documenttype", "versionnumber")
    
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

    ## PROJECT MEMBERSHIP ##
    # Using OuterRef & Subquery to perform a lookup against Tblproject on Tbluserproject's projectnumber and add it to the model with annotate 
    firstnames = Tbluser.objects.filter(
        validto__isnull=True
        ,usernumber=OuterRef("usernumber")
    ).values("firstname")

    lastnames = Tbluser.objects.filter(
        validto__isnull=True
        ,usernumber=OuterRef("usernumber")
    ).values("lastname")

    project_membership = Tbluserproject.objects.filter(
            validto__isnull=True
            , projectnumber=projectnumber
    ).values(
    ).annotate(firstname = Subquery(firstnames)
               ,lastname = Subquery(lastnames)
    ).order_by("firstname", "lastname")

    ## KRISTAL REFERENCES ##
    kristal_refs = Tblkristal.objects.filter(
        kristalnumber__in = Tblprojectkristal.objects.filter(
            validto__isnull=True
            , projectnumber=projectnumber
            )
        ,validto__isnull=True
    ).values(
    ).order_by("kristalref")

    ## DAT ALLOCATION ##
    project_dat_allocation = Tblprojectdatallocation.objects.filter(
        validto__isnull=True
        , projectnumber=projectnumber
    ).values("projectdatallocationid", "fromdate", "todate", "fte", "account"
    ).order_by("-fromdate")

    ## PROJECT PLATFORM DETAILS ##
    project_platform_info = Tblprojectplatforminfo.objects.filter(
        validto__isnull=True
        , projectnumber=projectnumber
    ).values("projectplatforminfoid", "platforminfoid__platforminfodescription", "projectplatforminfo"
    ).order_by("platforminfoid", "projectplatforminfo")

    ## PROJECT NOTES ##
    query = request.GET.get("search_notes")
    filter_query = {}
    if query is not None and query != '':
        filter_query['pnote__icontains'] = query
    
    project_notes = Tblprojectnotes.objects.filter(
        Q(**filter_query, _connector=Q.OR)
        , projectnumber=projectnumber
    ).values(
    ).order_by("-created")

    paginator = Paginator(project_notes, 5)  # Show 5 posts per page
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    ## CREATE FORMS ##
    project_form = ProjectForm(initial=project, prefix='project')
    p_dat_allocation_form = ProjectDatAllocationForm(prefix='p_dat_allocation')
    p_notes_form = ProjectNotesForm(prefix='p_note')
    p_platform_info_form = ProjectPlatformInfoForm(prefix='p_platform')

    project_numbers = Tblproject.objects.filter(
        validto__isnull=True
    ).values("projectnumber"
    ).order_by("projectnumber")

    ## DATA VALIDATION ##
    # Populated on GET Request
    custom_errors = []

    ## SET CONTEXT ##
    context = {'project':project
        , 'form':project_form
        , 'project_numbers': project_numbers
        , 'new_note': p_notes_form
        , 'notes':page_obj
        , 'notes_filter' : query
        , 'members': project_membership
        , 'grants': kristal_refs
        , 'p_docs': p_docs
        , 'dat_allocation': project_dat_allocation
        , 'custom_errors': custom_errors
        , 'dat_allocation_form': p_dat_allocation_form
        , 'platforminfo': project_platform_info
        , 'platform_form': p_platform_info_form}

    # Then check if POST or GET

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
            else:
                context['form']=project_form

        elif 'p_dat_allocation-projectdatallocationid' in request.POST:
            p_dat_allocation_form = ProjectDatAllocationForm(request.POST, prefix='p_dat_allocation')
            if p_dat_allocation_form.is_valid():
                insert_dat_allocation = Tblprojectdatallocation(
                    projectnumber = projectnumber
                    ,fromdate = p_dat_allocation_form.cleaned_data['fromdate']
                    ,todate = p_dat_allocation_form.cleaned_data['todate']
                    ,fte = p_dat_allocation_form.cleaned_data['fte']
                    ,account = p_dat_allocation_form.cleaned_data['account']
                    ,validfrom = timezone.now()
                    ,createdby = request.user
                )
                insert_dat_allocation.save(force_insert=True)
                messages.success(request, 'DAT Allocation added successfully.')
                return HttpResponseRedirect(f"/project/{projectnumber}")
            else:
                context['dat_allocation_form']=p_dat_allocation_form

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
            else:
                context['new_note']=p_notes_form

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
            else:
                context['platform_form']=insert_platform_info

        return render(request, 'Prism/project.html', context)

    if request.method == 'GET':
        ## DATA VALIDATION ##
        # For information purposes only. 
        # Validation across/between forms or where errors not sufficient to prevent form submission.

        # Do we have a DAT Allocation?
        if not project_dat_allocation:
            custom_errors.append("Missing DAT Allocation information")

        # Are there missing accounts for DAT Recoveries?
        for item in project_dat_allocation:
            if item['account'] == '':
                custom_errors.append("Missing DAT Allocation Account information")
                break
        
        # Are there overlapping or missing periods of DAT Support?
        if project_dat_allocation:
            df = pd.DataFrame(project_dat_allocation)
            Range = namedtuple('Range', ['start', 'end'])
            for index, row in df.iterrows():
                if index > 0:
                    r1 = Range(start=row['fromdate'], end=row['todate'])
                    r2 = Range(start=df['fromdate'].iloc[index-1], end=df['todate'].iloc[index-1])
                    latest_start = max(r1.start, r2.start)
                    earliest_end = min(r1.end, r2.end)
                    delta = (earliest_end - latest_start).days + 1
                    if delta > 0:
                        custom_errors.append("There are overlapping periods of DAT Allocation")
                    if delta < 0:
                        custom_errors.append("There are missing periods of DAT Allocation")
        
        # Does DAT Support period align with Project Start/End dates?
        if project_dat_allocation:
            earliest_dat_allocation = project_dat_allocation.order_by('fromdate').first()['fromdate']
            latest_dat_allocation = project_dat_allocation.order_by('todate').last()['todate']
            if project['projectedstartdate'] is not None and earliest_dat_allocation is not None and project['startdate'] is None:
                if earliest_dat_allocation > project['projectedstartdate']:
                    custom_errors.append("DAT Allocation starts after Projected Start Date")
                if earliest_dat_allocation < project['projectedstartdate']:
                    custom_errors.append("DAT Allocation starts before Projected Start Date")
            if project['projectedenddate'] is not None and latest_dat_allocation is not None and project['enddate'] is None:
                if latest_dat_allocation > project['projectedenddate']:
                    custom_errors.append("DAT Allocation continues after Projected End Date")
                if latest_dat_allocation < project['projectedenddate']:
                    custom_errors.append("DAT Allocation ends before Projected End Date")
            if project['startdate'] is not None and earliest_dat_allocation is not None:
                if earliest_dat_allocation > project['startdate']:
                    custom_errors.append("DAT Allocation starts after Start Date")
                if earliest_dat_allocation < project['startdate']:
                    custom_errors.append("DAT Allocation starts before Start Date")
            if project['enddate'] is not None and latest_dat_allocation is not None:
                if latest_dat_allocation > project['enddate']:
                    custom_errors.append("DAT Allocation ends after End Date")
                if latest_dat_allocation < project['enddate']:
                    custom_errors.append("DAT Allocation ends before End Date")

        # Do we have a Kristal Reference?
        if not kristal_refs:
            custom_errors.append("Missing Kristal Reference information")

        return render(request, 'Prism/project.html', context)

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
            return render(request, 'Prism/project_new.html', {'form':form})   

    if request.method == 'GET':
        form = ProjectForm()
        return render(request, 'Prism/project_new.html', {'form':form})
    
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
    
    ## DATA VALIDATION ##
    # Populated on GET Request
    custom_errors = []
    
    context = {'project_docs':project_docs
        , 'project_docs_form': project_docs_form
        , 'projectnumber':projectnumber
        , 'doctype':doctype_dict[doctype]
        , 'doctypeurl':doctype
        , 'custom_errors': custom_errors}
    
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
        else:
            context['project_docs_form'] = project_docs_form
        return render(request, 'Prism/docs.html', context)

    if request.method == "GET":
        ## DATA VALIDATION ##
        # For information purposes only. 
        # Validation across/between forms or where errors not sufficient to prevent form submission.
        summary = project_docs.values('documenttype__documentdescription'
        ).annotate(
            accepted_count=Count('pdid', filter=Q(accepted__isnull=False), distinct=True)
            ,max_submitted=Max('submitted')
            ,max_accepted=Max('accepted')
        ).order_by()
        
        for doc_type in summary:
        # Is there > 1 Accepted for a Document Type?
            if doc_type['accepted_count'] > 1:
                custom_errors.append(f"There is more than one Accepted {doc_type['documenttype__documentdescription']}")
        # Is there a Submitted later than an Accepted?
            if doc_type['max_submitted'] is not None and doc_type['max_accepted'] is not None:
                if doc_type['max_submitted'] > doc_type['max_accepted']:
                    custom_errors.append(f"A {doc_type['documenttype__documentdescription']} has been Submitted since the last Accepted")
        
        return render(request, 'Prism/docs.html', context)
    
def projectdocs_action(request, projectnumber, doctype, action, pdid):
    update_record=Tblprojectdocument.objects.filter(
        pdid=pdid
        , projectnumber=projectnumber
    ).values()

    if action == 'accept':
        update_record.update(accepted = timezone.now())
    elif action == 'withdraw':
        update_record.update(accepted = None)
    elif action == 'remove':
        update_record.update(validto = timezone.now())
    
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

def projectdatallocation_remove(request, projectnumber, projectdatallocationid):
    update_record=Tblprojectdatallocation.objects.filter(
        projectdatallocationid=projectdatallocationid
        , projectnumber=projectnumber
    ).values()
    update_record.update(validto = timezone.now())
    
    return HttpResponseRedirect(f"/project/{projectnumber}")

def users(request):
    query = request.GET

    filter_query = {}
    advanced_filter_query = {}
    filter_list = []

    if query is not None and query != '':
        for key in query:
            value = query.get(key)
            if value != '':
                if key == 'q':
                    filter_query['firstname__icontains'] = value
                    filter_query['lastname__icontains'] = value
                    filter_list.append(f"First or Last Name contains '{value}'")
                if key == 'status_id':
                    advanced_filter_query['status__statusid__iexact'] = value
                    filter_list.append(f"Status is '{Tlkuserstatus.objects.get(statusid=value)}'")
                if key == 'username':
                    advanced_filter_query['username__icontains'] = value
                    filter_list.append(f"Username contains '{value}'")
                if key == 'email':
                    advanced_filter_query['email__icontains'] = value
                    filter_list.append(f"Email contains'{value}'")
                if key == 'organisation':
                    advanced_filter_query['organisation__icontains'] = value
                    filter_list.append(f"Organisation contains '{value}'")

    users = Tbluser.objects.filter(
            Q(**filter_query, _connector=Q.OR)
            , Q(**advanced_filter_query, _connector=Q.AND)
            , validto__isnull=True
        ).values(
            "userid"
            , "usernumber"
            , "status__statusdescription"
            , "firstname"
            , "lastname"
            , "email"
            , "username"
            , "organisation"
        ).order_by("lastname")

    filter_string = ", ".join(filter_list)
    user_search_form = UserSearchForm()

    return render(request, 'Prism/users.html', {'users': users
                                                   ,'user_form': user_search_form
                                                   ,'searchterms': filter_string})


def user(request, usernumber):
    # Build forms
    
    ## USER ##
    user = Tbluser.objects.filter(
        validto__isnull=True
        , usernumber=usernumber
    ).values(
    ).get()         # get() with no arguments will raise an exception if the queryset doesn't contain exactly one item

    # Using OuterRef & Subquery to perform a lookup against Tblproject on Tbluserproject's projectnumber and add it to the model with annotate 
    projectnames = Tblproject.objects.filter(
        validto__isnull=True
        ,projectnumber=OuterRef("projectnumber")
    ).values("projectname")

    user_project = Tbluserproject.objects.filter(
        validto__isnull=True
        , usernumber=usernumber
    ).values(
    ).annotate(projectname = Subquery(projectnames)
    ).order_by("projectnumber")

    ## USER NOTES ##
    query = request.GET.get("search_notes")
    filter_query = {}
    if query is not None and query != '':
        filter_query['unote__icontains'] = query
    
    user_notes = Tblusernotes.objects.filter(
        Q(**filter_query, _connector=Q.OR)
        , usernumber=usernumber
    ).values(
    ).order_by("-created")

    paginator = Paginator(user_notes, 5)  # Show 5 posts per page
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    ## CREATE FORMS ##
    user_form = UserForm(initial=user, prefix='user')
    user_project_form = UserProjectForm(prefix='user_project')
    user_project_form.initial['usernumber'] = usernumber
    u_notes_form = UserNotesForm(prefix='u_note')
    
    context={'user': user
            , 'user_form': user_form
            , 'user_project': user_project
            , 'user_project_form': user_project_form
            , 'notes':page_obj
            , 'notes_filter' : query
            , 'new_note': u_notes_form
             }

    if request.method == 'POST':
        if 'user-userid' in request.POST:
            user_form = UserForm(request.POST, prefix='user')
            if user_form.is_valid():
                userid = user_form.cleaned_data['userid']
                insert = Tbluser(
                    usernumber = usernumber
                    ,status = user_form.cleaned_data['status_id']
                    ,firstname = user_form.cleaned_data['firstname']
                    ,lastname = user_form.cleaned_data['lastname']
                    ,email = user_form.cleaned_data['email']
                    ,phone = user_form.cleaned_data['phone']
                    ,username = user_form.cleaned_data['username']
                    ,organisation = user_form.cleaned_data['organisation']
                    ,startdate = user_form.cleaned_data['startdate']
                    ,enddate = user_form.cleaned_data['enddate']
                    ,laseragreement = user_form.cleaned_data['laseragreement']
                    ,dataprotection = user_form.cleaned_data['dataprotection']
                    ,informationsecurity = user_form.cleaned_data['informationsecurity']
                    ,safe = user_form.cleaned_data['safe']
                    ,validfrom = timezone.now()
                    ,validto = None
                    ,createdby = request.user
                )
                
                # Fetch existing user record
                existing_user = Tbluser.objects.filter(
                    validto__isnull=True
                    , usernumber=usernumber
                ).values(
                ).get() 

                # Only save record if fields have changed
                if recordchanged(existing_record=existing_user, form_set=insert):
                    insert.save(force_insert=True)

                    delete = Tbluser(
                        userid = userid
                        ,validto = timezone.now()
                    )
                    delete.save(update_fields=["validto"])
                
                    messages.success(request, 'User updated successfully.')
                return HttpResponseRedirect(f"/user/{usernumber}")
            else:
                context['user']=user_form

        elif 'user_project-projectnumber' in request.POST:
            user_project_form = UserProjectForm(request.POST, prefix='user_project')

            if user_project_form.is_valid():
                insert_user_project = Tbluserproject(
                    usernumber = user_project_form.cleaned_data['usernumber']
                    ,projectnumber = user_project_form.cleaned_data['projectnumber']
                    ,validfrom = timezone.now()
                    ,validto = None
                    ,createdby = request.user
                )
                insert_user_project.save(force_insert=True)
                messages.success(request, 'User Project membership added successfully.')
                return HttpResponseRedirect(f"/user/{usernumber}")
            else:
                context['user_project_form']=user_project_form

        elif 'u_note-unote' in request.POST:
            u_notes_form = UserNotesForm(request.POST, prefix='u_note')
            if u_notes_form.is_valid():
                insert_note = Tblusernotes(
                    usernumber = usernumber
                    ,unote = u_notes_form.cleaned_data['unote']
                    ,created = timezone.now()
                    ,createdby = request.user
                )
                insert_note.save(force_insert=True)
                messages.success(request, 'User note added successfully.')
                return HttpResponseRedirect(f"/user/{usernumber}")
            else:
                context['new_note']=u_notes_form

        return render(request, 'Prism/user.html', context)

    if request.method == 'GET':
        return render(request, 'Prism/user.html', context)

def userproject_remove(request, usernumber, userprojectid):
    update_record=Tbluserproject.objects.filter(
        userprojectid=userprojectid
        , usernumber=usernumber
    ).values()
    update_record.update(validto = timezone.now())
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))