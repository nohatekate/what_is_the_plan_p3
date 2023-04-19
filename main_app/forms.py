from django.forms import ModelForm
from .models import Group

class CreateGroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ['name']