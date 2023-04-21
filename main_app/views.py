from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import View
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Group, Idea
from .forms import CreateGroupForm
from .forms import IdeaForm


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

@login_required
def groups_index(request):
    groups = Group.objects.all()
    # groups = Group.objects.filter(user=request.user)
    return render(request, 'groups/index.html', {'groups': groups})

@login_required
def groups_detail(request, group_id):
    group = Group.objects.get(id=group_id)
    idea_form = IdeaForm()
    return render(request, 'groups/detail.html', { 'group': group, 'idea_form': idea_form})

@login_required
def add_idea(request, group_id):
    form = IdeaForm(request.POST)
    print("We made it to add_idea")
    if form.is_valid():
        print("we're check validity")
        new_idea = form.save(commit=False)
        print(group_id)
        new_idea.group_id = group_id 
        new_idea.save()
        print("we're saved")
    return redirect('detail', group_id=group_id)

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

class GroupCreate(LoginRequiredMixin, CreateView):
    model = Group
    fields = ['name']

    def form_valid(self, form):
        form.instance.user = self.request.user  

        return super().form_valid(form)
    
class GroupUpdate(LoginRequiredMixin, UpdateView):
    model = Group
    fields = ['name']
    
class GroupDelete(LoginRequiredMixin, DeleteView):
    model = Group
    success_url = '/groups'

class IdeaDelete(LoginRequiredMixin, View): 
    def get(self, request, *args, **kwargs):
        idea = Idea.objects.get(id=kwargs['pk'])
        idea.delete()
        return redirect('detail', group_id=kwargs['group_id'])
