from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('groups/', views.groups_index, name='index'),
    path('groups/<int:group_id>/', views.groups_detail, name='detail'),
    path('groups/create/', views.GroupCreate.as_view(), name='groups_create'),
    path('accounts/signup/', views.signup, name='signup'),
]
