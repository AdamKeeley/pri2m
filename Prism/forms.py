from django import forms
from .models import Tlkstage, Tblproject, Tlkclassification, Tlkfaculty, Tbluser, Tblprojectnotes, Tblprojectdocument, Tlkdocuments, Tblprojectplatforminfo, Tlkplatforminfo, Tblprojectdatallocation
from django.utils import timezone
from django.core.exceptions import ValidationError

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
        projectedstartdate = cleaned_data.get("projectedstartdate")
        projectedenddate = cleaned_data.get("projectedenddate")

        if (projectedstartdate - projectedenddate).days > 0:
            raise ValidationError(
                    "Start Date cannot be later than End Date."
                )
        return self.cleaned_data
        
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

        if (fromdate - todate).days > 0:
            raise ValidationError(
                    "To Date cannot be earlier than From Date."
                )

    class Meta:
        model=Tblprojectdatallocation