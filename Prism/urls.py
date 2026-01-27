from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index')
    ,path('projects', views.projects, name = 'projects')
    ,path('project/<str:projectnumber>', views.project, name = 'project')
    ,path('projectcreate', views.projectcreate, name = 'projectcreate')
    ,path('project/<str:projectnumber>/docs', views.projectdocs, name = 'projectdocs')
    ,path('project/<str:projectnumber>/docs/<str:doctype>', views.projectdocs, name = 'projectdocs')
    ,path('project/<str:projectnumber>/docs/<str:doctype>/<str:action>/<int:pdid>', views.projectdocs_action, name = 'projectdocs_action')
    ,path('project/<str:projectnumber>/remove/platform/<int:projectplatforminfoid>', views.projectplatforminfo_remove, name = 'projectplatforminfo_remove')
    ,path('project/<str:projectnumber>/remove/datallocation/<int:projectdatallocationid>', views.projectdatallocation_remove, name = 'projectdatallocation_remove')
    ,path('users', views.users, name = 'users')
    ,path('user/<int:usernumber>', views.user, name = 'user')
    ,path('usercreate', views.usercreate, name = 'usercreate')
    ,path('user/<int:usernumber>/remove/userproject/<int:userprojectid>', views.userproject_remove, name = 'userproject_remove')
]