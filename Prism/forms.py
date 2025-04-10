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
    stage= forms.ModelChoiceField(queryset=Tlkstage.objects.values_list("pstagedescription", flat=True
                                                                        ).filter(validto__isnull=True
                                                                        ).order_by("stagenumber"
                                                                        ), to_field_name='stageid')
    classification= forms.ModelChoiceField(queryset=Tlkclassification.objects.values_list("classificationdescription", flat=True
                                                                        ).filter(validto__isnull=True
                                                                        ).order_by("classificationdescription"
                                                                        ), to_field_name='classificationid')
    projectedstartdate= forms.DateField()
    projectedenddate= forms.DateField()
    startdate= forms.DateField()
    enddate= forms.DateField()
    pi_fullname= forms.CharField(max_length=50)
    leadapplicant_fullname= forms.CharField(max_length=50)
    faculty= forms.ModelChoiceField(queryset=Tlkfaculty.objects.values_list("facultydescription", flat=True
                                                                        ).filter(validto__isnull=True
                                                                        ).order_by("facultydescription"
                                                                        ), to_field_name='facultyid')
    lida= forms.BooleanField(label="LIDA")
    internship= forms.BooleanField(label="DSDP")
    dspt= forms.BooleanField(label="NHS DSPT")
    iso27001= forms.BooleanField(label="ISO27001")
    laser= forms.BooleanField(label="LASER")
    irc= forms.BooleanField(label="IRC")
    seed= forms.BooleanField(label="SEED")

    '''
    https://www.webforefront.com/django/formprocessing.html
    listing 6-11 for the win!
    '''

    def __init__(self, *args, **kwargs):
        initial_arguments = kwargs.get('initial', None)
        updated_initial = initial_arguments
        if initial_arguments:
            stage = initial_arguments.get('stage__pstagedescription',None)
            if stage:
                    updated_initial['stage'] = stage
            classification = initial_arguments.get('classification__classificationdescription',None)
            if classification:
                    updated_initial['classification'] = classification
            faculty = initial_arguments.get('faculty__facultydescription',None)
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