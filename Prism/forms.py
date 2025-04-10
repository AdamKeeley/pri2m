from django import forms
from .models import Tlkstage, Tblproject


class ProjectForm(forms.Form):
    projectnumber= forms.CharField(max_length=5)
    projectname= forms.CharField(max_length=500)
    stage= forms.ModelChoiceField(queryset=Tlkstage.objects.values_list("pstagedescription", flat=True
                                                                        ).filter(validto__isnull=True
                                                                        ).order_by("stagenumber"
                                                                        ), to_field_name='stageid')             # Need to get options from model
    classification= forms.ChoiceField()     # Need to get options from model
    projectedstartdate= forms.DateField()
    projectedenddate= forms.DateField()
    startdate= forms.DateField()
    enddate= forms.DateField()
    pi_fullname= forms.CharField(max_length=50)
    leadapplicant_fullname= forms.CharField(max_length=50)
    faculty= forms.ChoiceField()            # Need to get options from model
    lida= forms.CheckboxInput()
    internship= forms.CheckboxInput()
    dspt= forms.CheckboxInput()
    iso27001= forms.CheckboxInput()
    laser= forms.CheckboxInput()
    irc= forms.CheckboxInput()
    seed= forms.CheckboxInput()
    validfrom= forms.DateField()
    validto= forms.DateField()
    createdby= forms.CharField(max_length=50)

    '''
    https://www.webforefront.com/django/formprocessing.html
    listing 6-11 for the win!
    '''

    def __init__(self, *args, **kwargs):
                initial_arguments = kwargs.get('initial', None)
                updated_initial = {}
                if initial_arguments:
                    stage = initial_arguments.get('stage__pstagedescription',None)
                    if stage:
                          updated_initial['stage'] = stage

                kwargs.update(initial=updated_initial)
                super(ProjectForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Tblproject