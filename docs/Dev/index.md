---
layout: default
title: Django initiation
nav_order: 1
has_children: false
---

# Useful resources
Getting started:
[https://absolutecodeworks.com/python-django-crud-sample-with-sql-server](https://absolutecodeworks.com/python-django-crud-sample-with-sql-server)

Database connectivity:
[https://djangoadventures.com/how-to-integrate-django-with-existing-database/](https://djangoadventures.com/how-to-integrate-django-with-existing-database/)

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

# Connect to existing database and create models

Need to install `mssql-django` package to connect to Azure SQL Database, Django built-in database backends only include postgresql, mysql, sqlite3 & oracle.

Edit Project settings.py and set DATABASES to point to existing database:  
```python
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': <db_name>,
        'USER': <user_name>,
        'PASSWORD': <password>,
        'HOST': <server_name>'.database.windows.net',
        'PORT': '',
        'OPTIONS': {
            'driver': 'ODBC Driver 18 for SQL Server',
        }
    }
}
```

Automagically create Django models for all tables in existing database:  
```python 
python manage.py inspectdb > models.py
```

Once gernerated need to check to ensure foriegn key 'on_delete' behaviour is proper. It wasn't for me, so changed all `DO_NOTHING` to `PROTECT` (which is Django equivalent of SQL `RESTRICT`).  

For Django to manage table schema automatically, need to remove the `managed` attribute from each generated model. I don't want to do this just yet, if ever...

Place the `models.py` file in the App directory. 

Django automagically creates the migrations scripts:  
```python
python manage.py makemigrations
```

To apply the scripts run:
```python
python manage.py migrate --fake-initial
```  
The `--fake-initial` flag lets Django skip migrations where the table already exists. 

The Django user needs permissions to create the django_migrations table on first run.  

Now we should be running as if Django was managing the database from the start...
