---
layout: default
title: Django initiation
nav_order: 1
has_children: false
---

- TOC
{:toc}

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

Start the server with: 
```python
python manage.py runserver
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

# Models & Views

Because we're now using Django models to define the SQL tables, we can leverage foreign keys to present values instead of keys.  

To do this, when querying the model from the view, append `__lookupTableFieldName` to the fact table field name. for example,  

```python
def projects(request):
    projects = Tblproject.objects.filter(
            validto__isnull=True
        ).values(
            "pid"
            , "projectnumber"
            , "projectname"
            , "stage__pstagedescription"
            , "pi"
            , "faculty__facultydescription"
        ).order_by("projectnumber")
    return render(request, 'projects.html', {'projects':projects})
```

To define relationships between models for which no foreign key on the database is possible, eg `pi`, simply need to define the field as a `ForeignKey` in the model and use the `db_constraint=False` flag.  

Use `.annotate()` to add fields to query resultsets in view. For example can create `fullname` field from `firstname` & `lastname`. Don't even need to include `firstname` & `lastname` in teh returned resultset.  
```python
from django.db.models import Value
from django.db.models.functions import Concat
...
.annotate(
            pi_fullname = Concat('pi__firstname', Value(' '), 'pi__lastname')
        )
```

# Forms

`ModelChoiceField` takes actual model objects, do not use `.values` or `values_list`.  
It uses the primary keys of the model objects for key values and their string representation as their label values.  
In order to not have keys for label we need to override the string representations in the model:
```python
class Tlkstage(models.Model):
    stageid = models.IntegerField(db_column='StageID', primary_key=True) 
    stagedescription = models.CharField(db_column='pStageDescription', max_length=25)

    def __str__(self):
        return self.stagedescription
```

`DateField` seems to default to text when rendered to html!  
To render as actual date pickers we can override their widgets in `__init__`, after creating a `DateInput` class:
```python
class DateInput(forms.DateInput):
    input_type = "date"
    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%d"
        super().__init__(**kwargs)

class MyForm(forms.Form):
    ...
    def __init__(self, *args, **kwargs):
        self.fields["datefield"].widget = DateInput()
```

Form fields can be prepopulated with details from a queryset using the `initial` argument when instantiating the form in the view.  
```python
form = MyForm(initial=queryset)
```

Some form fields seem to struggle with this when the field value comes from a `ForeignKey` field in the model, noticeably `ModelChoiceField`. This can be overcome by overriding the `initial` arguments in the `__init__` of the form:
```python
class MyForm(forms.Form):
    ...
    def __init__(self, *args, **kwargs):
        initial_arguments = kwargs.get('initial', None)
        updated_initial = initial_arguments
        if initial_arguments:
            formfield = initial_arguments.get('formfield_id',None)
            if formfield:
                    updated_initial['formfield'] = formfield
        kwargs.update(initial=updated_initial)
        super(ProjectForm, self).__init__(*args, **kwargs)
```

# CRUD

Started off writing my own SQL and using Django's RAW Execute to run it, but quickly decided I'd rather use the Django-centric ORM to manipulate the db. 

Went absolutely doo-lally with repeated integrity errors, seemingly caused by Django trying to insert on an identity field. Took me far too long to check that the primary key on the database table actually was an `identity` field. Turned out it wasn't! 

Remade the table and now the Django model data type `AutoField` actually works as expected. 
- if a primary key is on database table as `identity(1,1)` the value is generated by the database sequentially
- if that same primary key is defined in the Django model as `AutoField` Django will let the value be generated by the database
- and if noone knows who should be generating the primary key values unhappiness ensues...

Updates are passed to `model.save(forced_insert=True)` without a primary key assignation because I want to maintain the existing Type 2 SDC on data in Prism.  
After each insert we then run an update on the pre-existing record to set `ValidTo` to `now()`, effecting the logical delete.  

From the docs: [https://docs.djangoproject.com/en/5.1/ref/models/instances/](https://docs.djangoproject.com/en/5.1/ref/models/instances/)  
>    If the object’s primary key attribute is set to anything except None, Django executes an UPDATE.  
>
>   If the object’s primary key attribute is not set or if the UPDATE didn’t update anything (e.g. if primary key is set to a value that doesn’t exist in the database), Django executes an INSERT.  

So when `POST`ing project updates the pID primary key field is omitted from the model object that is then used for the .save() action, and when logically deleting the previous record it is just one of the two fields used (`pID` & `ValidTo`).  