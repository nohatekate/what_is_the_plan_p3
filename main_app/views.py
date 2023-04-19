from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import Group

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

class GroupCreate(CreateView):
    model = Group
    fields = '__all__'
    success_url = '/groups'