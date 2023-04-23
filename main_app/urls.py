from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('groups/', views.groups_index, name='index'),
    path('groups/<int:group_id>/', views.groups_detail, name='detail'),
    path('groups/create/', views.GroupCreate.as_view(), name='groups_create'),
    path('groups/<int:pk>/update/', views.GroupUpdate.as_view(), name='groups_update'),
    path('groups/<int:pk>/delete/', views.GroupDelete.as_view(), name='groups_delete'),
    path('groups/<int:group_id>/add_idea/', views.add_idea, name='add_idea'),

    path('groups/<int:group_id>/ideas/<int:pk>/delete/', views.IdeaDelete.as_view(), name='ideas_delete'),

    path('accounts/signup/', views.signup, name='signup'),

    path('groups/<int:group_id>/choose_random_idea/', views.choose_random_idea, name='choose_random_idea'),

    path('groups/<int:group_id>/add_photo/', views.add_photo, name='add_photo'),
]
