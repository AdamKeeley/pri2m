from django import forms
from .models import Tlkstage, Tblproject, Tlkclassification, Tlkfaculty, Tbluser

class DateInput(forms.DateInput):
    input_type = "date"
    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%d"
        super().__init__(**kwargs)


class ProjectForm(forms.Form):
    pid = forms.IntegerField(widget = forms.HiddenInput(), required=False)
    projectnumber= forms.CharField(label="Project Number", disabled=True, max_length=5, required=False)
    projectname= forms.CharField(label="Project Name", max_length=500)
    portfolionumber = forms.CharField(label="Portfolio Number", widget = forms.HiddenInput(), required=False, max_length=255)
    stage_id= forms.ModelChoiceField(label="Stage", queryset=Tlkstage.objects.filter(validto__isnull=True).order_by("stagenumber"))
    classification_id= forms.ModelChoiceField(label="Classification", queryset=Tlkclassification.objects.filter(validto__isnull=True).order_by("classificationdescription"))
    datrag = forms.IntegerField(label="DAT RAG", widget = forms.HiddenInput(), required=False)
    projectedstartdate= forms.DateField(label="Projected Start Date")
    projectedenddate= forms.DateField(label="Projected End Date")
    startdate= forms.DateField(label="Start Date", required=False)
    enddate= forms.DateField(label="End Date", required=False)
    pi = forms.ModelChoiceField(label="PI", queryset=Tbluser.objects.filter(validto__isnull=True).order_by("firstname", "lastname"), to_field_name="usernumber")
    leadapplicant= forms.ModelChoiceField(label="Lead Applicant", queryset=Tbluser.objects.filter(validto__isnull=True).order_by("firstname", "lastname"), to_field_name="usernumber")
    faculty_id= forms.ModelChoiceField(label="Faculty", queryset=Tlkfaculty.objects.filter(validto__isnull=True).order_by("facultydescription"))
    lida= forms.BooleanField(label="LIDA", required=False)
    internship= forms.BooleanField(label="DSDP", required=False)
    dspt= forms.BooleanField(label="NHS DSPT", required=False)
    iso27001= forms.BooleanField(label="ISO27001", required=False)
    laser= forms.BooleanField(label="LASER", required=False)
    irc= forms.BooleanField(label="IRC", required=False)
    seed= forms.BooleanField(label="SEED", required=False)
    validfrom=  forms.DateTimeField(widget = forms.HiddenInput(), required=False) 
    validto= forms.DateTimeField(widget = forms.HiddenInput(), required=False)
    createdby= forms.CharField(widget = forms.HiddenInput(), required=False, max_length=50)

    '''
    https://www.webforefront.com/django/formprocessing.html
    listing 6-11 for the win!
    '''

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        self.fields["projectedstartdate"].widget = DateInput()
        self.fields["projectedenddate"].widget = DateInput()
        self.fields["startdate"].widget = DateInput()
        self.fields["enddate"].widget = DateInput()

    class Meta:
        model = Tblproject