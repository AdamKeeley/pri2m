from django import forms


class ProjectForm(forms.Form):
    projectnumber= forms.CharField(max_length=5)
    projectname= forms.CharField(max_length=500)
    stage= forms.ChoiceField()              # Need to get options from model
    classification= forms.ChoiceField()     # Need to get options from model
    projectedstartdate= forms.DateField()
    projectedenddate= forms.DateField()
    startdate= forms.DateField()
    enddate= forms.DateField()
    pi= forms.ChoiceField()                 # Need to get options from model
    leadapplicant= forms.ChoiceField()      # Need to get options from model
    faculty= forms.ChoiceField()            # Need to get options from model
    lida= forms.CheckboxInput
    internship= forms.CheckboxInput
    dspt= forms.CheckboxInput
    iso27001= forms.CheckboxInput
    laser= forms.CheckboxInput
    irc= forms.CheckboxInput
    seed= forms.CheckboxInput
    validfrom= forms.DateField()
    validto= forms.DateField()
    createdby= forms.CharField(max_length=50)