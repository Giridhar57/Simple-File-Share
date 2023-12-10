from django.forms import ModelForm
from .models import Files

class FilesForm(ModelForm):
    class Meta: 
        model = Files
        fields = ['name','file']