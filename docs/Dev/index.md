---
layout: default
title: Django initiation
nav_order: 1
has_children: false
---

# Useful resources
[https://absolutecodeworks.com/python-django-crud-sample-with-sql-server](https://absolutecodeworks.com/python-django-crud-sample-with-sql-server)

# First steps!

Create a conda env and installed pyodbc and django, generate a requirements.txt. Will need other packages I'm sure.

Create Django Project (LASER)  
```python
django-admin startproject LASER .
```

Create Django App (Prism)  

```python
python manage.py startapp Prism
```

Add Prism app to list of `INSTALLED_APPS` in Project settings.py  
```python
INSTALLED_APPS = [
    ...
    'Prism',
]
```

Create html template file (/templates/projects.html)


Add view of `projects.html` to views.py
```python
def projects(request):
    return render(request, 'projects.html')
```

Create urls.py in App directory (/Prism)  
```python
from django.urls import path
from . import views
urlpatterns = [
    path('', views.projects, name = 'projects')
]
```

Add reference to App URLs (urls.py) in Project URLs (urls.py).
Need to import `include` function from `django.urls`. 
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Prism.urls'))
]
```