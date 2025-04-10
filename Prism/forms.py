from django import forms
from .models import Tlkstage, Tblproject, Tlkclassification, Tlkfaculty

class DateInput(forms.DateInput):
    input_type = "date"
    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%d"
        super().__init__(**kwargs)

class ProjectForm(forms.Form):
    projectnumber= forms.CharField(max_length=5)
    projectname= forms.CharField(max_length=500)
    stage= forms.ModelChoiceField(queryset=Tlkstage.objects.filter(validto__isnull=True).order_by("stagenumber"))
    classification= forms.ModelChoiceField(queryset=Tlkclassification.objects.filter(validto__isnull=True).order_by("classificationdescription"))
    projectedstartdate= forms.DateField()
    projectedenddate= forms.DateField()
    startdate= forms.DateField(required=False)
    enddate= forms.DateField(required=False)
    pi_fullname= forms.CharField(max_length=50)
    leadapplicant_fullname= forms.CharField(max_length=50)
    faculty= forms.ModelChoiceField(queryset=Tlkfaculty.objects.filter(validto__isnull=True).order_by("facultydescription"))
    lida= forms.BooleanField(label="LIDA", required=False)
    internship= forms.BooleanField(label="DSDP", required=False)
    dspt= forms.BooleanField(label="NHS DSPT", required=False)
    iso27001= forms.BooleanField(label="ISO27001", required=False)
    laser= forms.BooleanField(label="LASER", required=False)
    irc= forms.BooleanField(label="IRC", required=False)
    seed= forms.BooleanField(label="SEED", required=False)

    '''
    https://www.webforefront.com/django/formprocessing.html
    listing 6-11 for the win!
    '''

    def __init__(self, *args, **kwargs):
        initial_arguments = kwargs.get('initial', None)
        updated_initial = initial_arguments
        if initial_arguments:
            stage = initial_arguments.get('stage_id',None)
            if stage:
                    updated_initial['stage'] = stage
            classification = initial_arguments.get('classification_id',None)
            if classification:
                    updated_initial['classification'] = classification
            faculty = initial_arguments.get('faculty_id',None)
            if faculty:
                    updated_initial['faculty'] = faculty
        kwargs.update(initial=updated_initial)
        
        super(ProjectForm, self).__init__(*args, **kwargs)

        self.fields["projectedstartdate"].widget = DateInput()
        self.fields["projectedenddate"].widget = DateInput()
        self.fields["startdate"].widget = DateInput()
        self.fields["enddate"].widget = DateInput()

    class Meta:
        model = Tblproject