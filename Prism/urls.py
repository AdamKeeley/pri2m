from django.urls import path
from . import views

urlpatterns = [
    path('', views.projects, name = 'projects'),
    path('project/<str:projectnumber>', views.project, name = 'project'),
    path('project/delete/<str:projectnumber>', views.projectdelete, name = 'projectdelete')
]