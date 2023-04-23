import uuid
import boto3
import os
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import View
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import random

from .models import Group, Idea, Photo
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
    return render(request, 'groups/detail.html', { 'group': group, 'idea_form': idea_form })

@login_required
def add_idea(request, group_id):
    form = IdeaForm(request.POST)
    if form.is_valid():
        new_idea = form.save(commit=False)
        new_idea.group_id = group_id 
        new_idea.save()
    return redirect('detail', group_id=group_id)

@login_required
def choose_random_idea(request, group_id):
    group = Group.objects.get(id=group_id)
    ideas = Idea.objects.filter(group=group_id)
    random_idea = random.choice(ideas)
    idea_form = IdeaForm()
    return render(request, 'groups/detail.html', { 'group': group, 'idea_form': idea_form, 'random_idea': random_idea })

@login_required
def add_photo(request, group_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            # build the full url string
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            Photo.objects.create(url=url, group_id=group_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
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
