from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

from .models import Group
from .forms import CreateGroupForm


# Create your views here.
# groups = [
#     {'name': 'Old Greg Goes Camping'},
#     {'name': 'FamBam'},
#     {'name': 'Blue Bubble Commune'},
#     {'name': 'Most of My Friends'},
#     {'name': 'Booze and Sweatpants'},
#     {'name': 'The Shits'}
# ]


def home(request):
    return render(request, 'home.html')

def groups_index(request):
    groups = Group.objects.all()
    # groups = Group.objects.filter(user=request.user)
    return render(request, 'groups/index.html', {'groups': groups})

def groups_detail(request, group_id):
    group = Group.objects.get(id=group_id)
    return render(request, 'groups/detail.html', { 'group': group})

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

class GroupCreate(CreateView):
    model = Group
    fields = ['name']

    def form_valid(self, form):
        form.instance.user = self.request.user  

        return super().form_valid(form)