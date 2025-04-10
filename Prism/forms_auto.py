from django.forms import ModelForm
from . import models

# Create the form class.
class ProjectForm(ModelForm):
    class Meta:
        model = models.Tblproject
        fields = '__all__'