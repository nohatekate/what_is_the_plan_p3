from django.forms import ModelForm
from .models import Group
from .models import Idea

class CreateGroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ['name']

class IdeaForm(ModelForm):
    class Meta:
        model = Idea
        fields = ['name', 'environment', 'estimated cost']