from django import forms
from .models import Tlkstage, Tblproject, Tlkclassification, Tlkfaculty, Tbluser, Tblprojectnotes, Tblprojectdocument \
    , Tlkdocuments, Tblprojectplatforminfo, Tlkplatforminfo, Tblprojectdatallocation, Tlkuserstatus, Tlktitle, Tbluserproject \
    , tblusernotes
from django.utils import timezone
#from django.core.exceptions import ValidationError

class DateInput(forms.DateInput):
    input_type = "date"
    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%d"
        super().__init__(**kwargs)


class ProjectSearchForm(forms.Form):
    stage_id= forms.ModelChoiceField(label="Stage", queryset=Tlkstage.objects.filter(validto__isnull=True).order_by("stagenumber"), required=False)
    classification_id= forms.ModelChoiceField(label="Classification", queryset=Tlkclassification.objects.filter(validto__isnull=True).order_by("classificationdescription"), required=False)
    user = forms.ModelChoiceField(label="PI or Lead Applicant", queryset=Tbluser.objects.filter(validto__isnull=True).order_by("firstname", "lastname"), to_field_name="usernumber", required=False)
    faculty_id= forms.ModelChoiceField(label="Faculty", queryset=Tlkfaculty.objects.filter(validto__isnull=True).order_by("facultydescription"), required=False)
    laser= forms.BooleanField(label="LASER", required=False)
    internship= forms.BooleanField(label="DSDP", required=False)
        
    class Meta:
        model = Tblproject

class ProjectForm(forms.Form):
    pid = forms.IntegerField(widget = forms.HiddenInput(), required=False)
    projectnumber= forms.CharField(label="Project Number", disabled=True, max_length=5, required=False)
    projectname= forms.CharField(label="Project Name", max_length=500)
    portfolionumber = forms.CharField(label="Portfolio Number", widget = forms.HiddenInput(), required=False, max_length=255)
    stage_id= forms.ModelChoiceField(label="Stage", queryset=Tlkstage.objects.filter(validto__isnull=True).order_by("stagenumber"))
    classification_id= forms.ModelChoiceField(label="Classification", queryset=Tlkclassification.objects.filter(validto__isnull=True).order_by("classificationdescription"))
    datrag = forms.IntegerField(label="DAT RAG", widget = forms.HiddenInput(), required=False)
    projectedstartdate= forms.DateTimeField(label="Projected Start Date", widget = DateInput())
    projectedenddate= forms.DateTimeField(label="Projected End Date", widget = DateInput())
    startdate= forms.DateTimeField(label="Start Date", widget = DateInput(), required=False)
    enddate= forms.DateTimeField(label="End Date", widget = DateInput(), required=False)
    pi = forms.ModelChoiceField(label="PI", queryset=Tbluser.objects.filter(validto__isnull=True).order_by("firstname", "lastname"), to_field_name="usernumber")
    leadapplicant= forms.ModelChoiceField(label="Lead Applicant", queryset=Tbluser.objects.filter(validto__isnull=True).order_by("firstname", "lastname"), to_field_name="usernumber")
    faculty_id= forms.ModelChoiceField(label="Faculty", queryset=Tlkfaculty.objects.filter(validto__isnull=True).order_by("facultydescription"))
    lida= forms.BooleanField(label="LIDA", required=False, initial=True)
    internship= forms.BooleanField(label="DSDP", required=False)
    dspt= forms.BooleanField(label="NHS DSPT", required=False)
    iso27001= forms.BooleanField(label="ISO27001", required=False)
    laser= forms.BooleanField(label="LASER", required=False)
    irc= forms.BooleanField(label="IRC", required=False)
    seed= forms.BooleanField(label="SEED", required=False)
    validfrom=  forms.DateTimeField(widget = forms.HiddenInput(), required=False) 
    validto= forms.DateTimeField(widget = forms.HiddenInput(), required=False)
    createdby= forms.CharField(widget = forms.HiddenInput(), required=False, max_length=50)
    
    def clean(self):
        cleaned_data = super().clean()
        startdate = cleaned_data.get("startdate")
        enddate = cleaned_data.get("enddate")
        projectedstartdate = cleaned_data.get("projectedstartdate")
        projectedenddate = cleaned_data.get("projectedenddate")
        
        # Do project start and end dates sequence correctly?
        if projectedstartdate is not None and projectedenddate is not None:
            if (projectedstartdate - projectedenddate).days >= 0:
                self.add_error(None, "Projected Start Date cannot be later than Projected End Date.")
        if startdate is not None and enddate is not None:
            if (startdate - enddate).days >= 0:
                self.add_error(None, "Start Date cannot be later than End Date.")

        if "stage_id" in cleaned_data:
            stage = cleaned_data["stage_id"].pstagedescription
            # If Stage is Active/Store/Destroy do Start Date and End Date exist?
            if (stage == "Active" or stage == "Store") and startdate is None:
                self.add_error(None, "Project cannot have started without a Start Date")
            if (stage == "Destroy") and (enddate is None or startdate is None):
                self.add_error(None, "Project cannot End without both a Start and End Date")
            # If adding Start/End Dates does the Stage align?
            if startdate and (stage == "Proposal" or stage == "Pre-grant" or stage == "Pre-Approval" or stage == "Setup"):
                self.add_error(None, "Project cannot have a Start Date while in a pre-Active Stage")
            if enddate and not (stage == "Destroy" or stage == "Discontinued"):
                self.add_error(None, "Project cannot have a End Date without being in a Destroy or Discontinued Stage")

            if not self.fields["stage_id"].queryset.filter(validto__isnull=True, pk=cleaned_data['stage_id'].pk).exists():
                self.add_error('stage_id', "This value is no longer a valid choice.")

        return self.cleaned_data
        

    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)

        stage_qs = self.fields["stage_id"].queryset
        if 'initial' in kwargs:
            if not stage_qs.filter(pk=kwargs['initial']['stage_id']):
                self.fields["stage_id"].queryset = (stage_qs | Tlkstage.objects.filter(pk=kwargs['initial']['stage_id']))
        elif 'data' in kwargs:
            if not stage_qs.filter(pk=kwargs['data']['stage_id']):
                self.fields["stage_id"].queryset = (stage_qs | Tlkstage.objects.filter(pk=kwargs['data']['stage_id']))

        # When creating the form with initial data, we still want to validate the form. 
        # This `__init__` override will populate a temporary form (temp) with `data=initial` (as if POST) to trigger validation and 
        # therefore the `clean()` function above.
        # Any errors are copied to the original form and displayed with the data from the database.
        if self.initial: 
            temp = type(self)(data=self.initial) 
            if not temp.is_valid(): 
                self._errors = temp.errors

    class Meta:
        model = Tblproject

class ProjectNotesForm(forms.Form):
    pnid = forms.IntegerField(widget = forms.HiddenInput(), required=False)
    projectnumber = forms.CharField(widget = forms.HiddenInput(), label="Project Number", disabled=True, max_length=5, required=False)
    pnote = forms.CharField(widget=forms.Textarea(attrs={"rows":1, "placeholder": "New note..."}), label="Project Note", max_length=500)
    created = forms.DateTimeField(widget = forms.HiddenInput(), label="Created", disabled=True, required=False)
    createdby = forms.CharField(widget = forms.HiddenInput(), label="Created By", disabled=True, max_length=50, required=False)

    class Meta:
        model = Tblprojectnotes

class ProjectDocumentsForm(forms.Form):
    pdid = forms.IntegerField(widget = forms.HiddenInput(), required=False)
    projectnumber = forms.CharField(widget = forms.HiddenInput(), label="Project Number", disabled=True, max_length=5, required=False)
    documenttype = forms.ModelChoiceField(label="Document Type", queryset=Tlkdocuments.objects.filter(validto__isnull=True).order_by("documentid"))
    versionnumber = forms.DecimalField(label="Version Number", widget= forms.HiddenInput() , required=False) #forms.NumberInput(attrs={'step': 1}))
    submitted = forms.DateTimeField(label="Submitted Date", widget = DateInput(), initial=timezone.now())
    accepted = forms.DateTimeField(label="Accepted Date", widget = DateInput(), required=False)
    validfrom = forms.DateTimeField(widget = forms.HiddenInput(), required=False)
    validto = forms.DateTimeField(widget = forms.HiddenInput(), required=False)
    createdby = forms.CharField(widget = forms.HiddenInput(), required=False, max_length=50)

    class meta:
        model=Tblprojectdocument

class ProjectPlatformInfoForm(forms.Form):
    projectplatforminfoid = forms.IntegerField(widget = forms.HiddenInput(), required=False)
    projectnumber = forms.CharField(widget = forms.HiddenInput(), label="Project Number", disabled=True, max_length=5, required=False)
    platforminfoid = forms.ModelChoiceField(label="Platform Item", queryset=Tlkplatforminfo.objects.filter(validto__isnull=True).order_by("platforminfoid"))
    projectplatforminfo = forms.CharField(label="Platform Info", widget=forms.Textarea(attrs={"rows":1, "placeholder": "Description..."}), max_length=255)
    validfrom = forms.DateTimeField(widget = forms.HiddenInput(), required=False)
    validto = forms.DateTimeField(widget = forms.HiddenInput(), required=False)
    createdby = forms.CharField(widget = forms.HiddenInput(), required=False, max_length=50)
    platforminfodescription = forms.CharField(label="Platform Info Description", max_length=25, required=False)

    class Meta:
        model=Tblprojectplatforminfo

class ProjectDatAllocationForm(forms.Form):
    projectdatallocationid = forms.IntegerField(widget = forms.HiddenInput(), required=False)
    projectnumber = forms.CharField(widget = forms.HiddenInput(), label="Project Number", disabled=True, max_length=5, required=False)
    fromdate = forms.DateTimeField(label="From Date", widget = DateInput(attrs={"placeholder": "From Date..."}))
    todate = forms.DateTimeField(label="To Date", widget = DateInput())
    duration = forms.DecimalField(label="Duration", widget= forms.HiddenInput() , required=False)
    durationcomputed = forms.DecimalField(label="Duration Computed", widget= forms.HiddenInput() , required=False)
    fte = forms.DecimalField(label="FTE", widget=forms.NumberInput(attrs={"placeholder": "FTE (min 2.5%)"}), required=True, min_value=2.5)
    account = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "UoL account to charge"}), label="Account code", max_length=25, required=False)
    validfrom = forms.DateTimeField(widget = forms.HiddenInput(), required=False)
    validto = forms.DateTimeField(widget = forms.HiddenInput(), required=False)
    createdby = forms.CharField(widget = forms.HiddenInput(), required=False, max_length=50)

    def clean(self):
        cleaned_data = super().clean()
        fromdate = cleaned_data.get("fromdate")
        todate = cleaned_data.get("todate")

        if (fromdate - todate).days >= 0:
            self.add_error(None, "To Date cannot be earlier than From Date.")
        return self.cleaned_data

    class Meta:
        model=Tblprojectdatallocation

class UserSearchForm(forms.Form):
    status_id = forms.ModelChoiceField(label="Status", queryset=Tlkuserstatus.objects.filter(validto__isnull=True).order_by("statusid"), required=False )
    username = forms.CharField(label="User Name", max_length=12, required=False)
    email = forms.CharField(label="Email", max_length=255, required=False) 
    organisation = forms.CharField(label="Organisation", max_length=255, required=False)

    class meta:
        model = Tbluser

class UserForm(forms.Form):
    userid = forms.IntegerField(widget = forms.HiddenInput(), required=False)
    usernumber = forms.IntegerField(widget = forms.HiddenInput(), required=False)
    status_id = forms.ModelChoiceField(label="Status", queryset=Tlkuserstatus.objects.filter(validto__isnull=True).order_by("statusid"), required=False )
    title_id = forms.ModelChoiceField(label='Title', queryset=Tlktitle.objects.filter(validto__isnull=True).order_by("titledescription"), required=False )
    firstname = forms.CharField(label="First Name", max_length=50)
    lastname = forms.CharField(label="Last Name", max_length=50)
    email = forms.CharField(label="Email", max_length=255, required=False) 
    phone = forms.CharField(label="Phone", max_length=15, required=False)
    username = forms.CharField(label="User Name", max_length=12, required=False)
    organisation = forms.CharField(label="Organisation", max_length=255)
    startdate = forms.DateTimeField(label="Start Date", widget = DateInput(), required=False)
    enddate = forms.DateTimeField(label="End Date", widget = DateInput(), required=False)
    # priviledged = forms.BooleanField(label="SEED Agreement", required=False)
    # seedagreement = forms.BooleanField(label="SEED Agreement", required=False)
    # ircagreement = forms.BooleanField(label="IRC Agreement", required=False)
    laseragreement = forms.DateTimeField(label="LASER Agreement", widget = DateInput(), required=False)
    dataprotection = forms.DateTimeField(label="Data Protection", widget = DateInput(), required=False)
    informationsecurity = forms.DateTimeField(label="Information Security", widget = DateInput(), required=False)
    # iset = forms.DateTimeField(label="ISET", widget = DateInput(), required=False)
    # isat = forms.DateTimeField(label="ISAT", widget = DateInput(), required=False)
    safe = forms.DateTimeField(label="Safe Researcher", widget = DateInput(), required=False)
    # tokenserial = forms.IntegerField(label="Token Serial", widget = forms.HiddenInput(), required=False)
    # tokenissued = forms.DateTimeField(label="Token Issued", widget = DateInput(), required=False)
    # tokenreturned = forms.DateTimeField(label="Token Returned", widget = DateInput(), required=False)
    validfrom=  forms.DateTimeField(widget = forms.HiddenInput(), required=False) 
    validto= forms.DateTimeField(widget = forms.HiddenInput(), required=False)
    createdby= forms.CharField(widget = forms.HiddenInput(), required=False, max_length=50)

    class meta:
        model = Tbluser

class UserProjectForm(forms.Form):
    userprojectid = forms.IntegerField(widget = forms.HiddenInput(), required=False)
    usernumber = forms.IntegerField(widget = forms.HiddenInput())
    projectnumber = forms.ModelChoiceField(label="Project Number", queryset=Tblproject.objects.filter(validto__isnull=True).order_by("projectnumber"))
    validfrom=  forms.DateTimeField(widget = forms.HiddenInput(), required=False) 
    validto= forms.DateTimeField(widget = forms.HiddenInput(), required=False)
    createdby= forms.CharField(widget = forms.HiddenInput(), required=False, max_length=50)

    def clean(self):
        cleaned_data = super().clean()
        projectnumber = cleaned_data.get('projectnumber')
        usernumber = cleaned_data.get('usernumber')

        if Tbluserproject.objects.filter(validto__isnull=True, usernumber=usernumber, projectnumber=projectnumber).exists():
            self.add_error(None, "User already on Project")

        return self.cleaned_data

    class meta:
        model = Tbluserproject

class UserNotesForm(forms.Form):
    unid = forms.IntegerField(widget = forms.HiddenInput(), required=False)
    usernumber = forms.CharField(widget = forms.HiddenInput(), label="User Number", disabled=True, max_length=5, required=False)
    unote = forms.CharField(widget=forms.Textarea(attrs={"rows":1, "placeholder": "New note..."}), label="User Note", max_length=500)
    created = forms.DateTimeField(widget = forms.HiddenInput(), label="Created", disabled=True, required=False)
    createdby = forms.CharField(widget = forms.HiddenInput(), label="Created By", disabled=True, max_length=50, required=False)

    class Meta:
        model = tblusernotes