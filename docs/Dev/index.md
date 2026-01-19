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

To do this, when querying the model from the view, append `__lookupTableFieldName` to the fact table field name. For example,  

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

It's possible to use `.annotate()` to add fields to query resultsets in view. For example can create `fullname` field from `firstname` & `lastname`. Don't even need to include `firstname` & `lastname` in the returned resultset. This only works if the fields you're using already exist in the database.  
```python
from django.db.models import Value
from django.db.models.functions import Concat
...
pi_user = Tbluser.objects.filter(
        validto__isnull=True
        , usernumber=project['pi']
    ).values(
        'usernumber'
    ).annotate(
        pi_fullname = Concat('firstname', Value(' '), 'lastname')
    ).get()
```

## Django relations and Type 2 SCD  
I've not found a way to define relationships between `Tbluser` model and user fields in the `Tblproject` model (eg `pi` and `leadapplicant`) whilst maintaining the desired Type 2 SCD behaviour of the database. The issue is that the primary key of `Tbluser` isn't used to identify an individual user; Type 2 SCD demands that we implement a surrogate key `usernumber` that's only unique when `validto` is null.  

I've tried defining the user fields of `Tblproject` as `ForeignKey` or `ManyToManyField` with a `db_constraint=False` flag but that just straight up didn't work.  

I've tried using a proxy table with custom methods to make data from `Tbluser` model available from an instance of `Tblproject` model in the View. That worked but the way Django functions it was necessary to iterate over every record in the view to populate and it seemed to make a database call every single time. The performance tanked and while it may be feasible for a single project, when listing many/all of them it was untenable.  

In the end I went with a single call to the model with the related data and converted it to a pandas DataFrame, using that to iterate over and update each record (eg replacing the `usernumber` value stored in `Tblproject.pi` with a concatenated full name in the `projects` view that lists all projects).  

Struggling to exclude model fields on SQL insert when updating records. I want to do this because I'd prefer the SQL Database to handle populating certain data fields like `ValidFrom` and `CreatedBy` with their database defaults, rather than having Django generate those values. Currently I am having to populate them in Django and insert the non-default values as all attempts at exclusion have just led to insertion of nulls... 


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

Some form fields seem to struggle with this when the field value comes from a `ForeignKey` field in the model, noticeably `ModelChoiceField`. ~~This can be overcome by overriding the `initial` arguments in the `__init__` of the form:~~  

<strike>

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

</strike>

While this did work it was utterly unneccessary! The real issue was simply that the fields in the form needed to be named to match the Primary Key of the related fields in the model. So, for example, the `stage` field in the `Tblproject` model is a ForeignKey to `Tlkstage`, which has the Primary Key `stage_id`. So declaring the `stage_id` field in the `ProjectForm` form (instead of `stage`) meant that it was able to receive current value from `initial`.  

Seems obvious now I look again at the code snippet above... I'm taking the value of `formfield_id` and popping it into `formfield`. Just use `formfield_id`!

`PI` & `LeadApplicant` fields are ModelChoiceFields again! They use a queryset from `Tbluser` model (with the overridden `__str__` frunction) to define permitted values and the flag `to_field_name="usernumber"` to prevent the use of the Primary Key for TblUser being used. Each Surrogate Key `usernumber` is (should be!) unique when `ValidTo` is null so need to ensure that's included in the filter defining the queryset. 

```python
pi = forms.ModelChoiceField(label="PI", queryset=Tbluser.objects.filter(validto__isnull=True).order_by("firstname", "lastname"), to_field_name="usernumber")
    
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


# Template inheritance  
Django lets us adhere to DRY principles in html templating through inheritance.  

By creating a top level html template that sets out styling and navigation, that all other templates inherit, consistency can be maintained. In this project the top level template is called `layout.html` and is saved with all the other html templates in `templates/Prism`.  

The `layout.html` template defines blocks that can be referenced in other html templates that inherit from it. In this way item positions and styles can be maintained across the site through the use of <!-- {% raw %} --> `{% block name %}{% endblock %}`<!-- {% endraw %} --> tags. All templates know to insert the content of these blocks into the corresponding block of the inherited template, as long as <!-- {% raw %} --> `{% extends "Prism/layout.html" %}`<!-- {% endraw %} --> is included at the top of the template.  

`layout.html` has been used to define the navigation bar at the top of the page. Because every page of the site inherits this template, every page of the site has the same nav bar and any changes to it need only be made once.  


# Static files  
A css style sheet has been created and is referenced in the parent template `layout.html` so all pages that inherit will be subject to the same styling choices. `style.css` has been saved to `static/Prism` along with a `prism.ico` favicon.  

Static files need to be loaded explicitly with <!-- {% raw %} --> `{% load static %}`<!-- {% endraw %} -->, but as this is done in the parent template it need only be done once here. When out of dev (ie when `DEBUG=False` in `settings.py`) there will be a need to load a third party library such as **WhiteNoise** to load static files.  


# Bootstrap 5
By installing `django-bootstrap-v5` to the python env we have access to bootstrap 5 styling.  

I've found this especially useful for laying out the controls using a grid (`col-md-auto` FTW), but I'm hoping it will come into it's own with comboboxes for named individuals on a project. The drop down boxes are kinda hard to use when dealing with so many options; we really need some form of autocomplete drop down.  


# Project Notes
We've had to establish multiple forms in a single view so that we can display and update project details and project notes on the same page.  

To do this we're instantiating forms `ProjectForm` and `ProjectNotesForm` with prefixes (`'project'` and `'p_note'` respectively). this prefixes all field names in the form with those values, so `ProjectForm.projectnumber` becomes `ProjectForm.project-projectnumber` for example. We can then use `if` statements on prefixed field names to conditionally split the workflow depending on which form is being submitted, eg:

```python
if request.method == "POST":
        if 'project-pid' in request.POST:
            # 
            # do project details stuff here
            # 
        elif 'p_note-pnote' in request.POST:
            # 
            # do project note stuff here
            # 
```

Make sure each form gets it's own <!-- {% raw %} --> `{% csrf_token %}`<!-- {% endraw %} --> to avoid Cross Site Request Forgery.  

The Notes form only has a single input control with a submit button all to itself. The notes themselves are displayed using an html table, iterating over an instance of the `Tblprojectnotes` model to populate.  

Pagination is a handy way to keep things readable and not clutter the screen; it is handled in the view.  

# Validation  

## Context setting  
Frequently we will want multiple forms to be displayed and submitted from a single page. For example, on a project page we will want to display project details from a `ProjectForm` instance with initial values populated and have it submit new values when changed. On the same page we would want those project details displayed alongside, for example, the project notes form (`ProjectNotesForm`) and have that populated with initial values and separately submittable.  

Multiple forms can be handles in the view for the page through the use of prefixes as described above. It does present a challenge when trying to redirect back to the page in the event of failed validation. The issue is that when redirecting from a failed form validation the context for the page is missing. This results in the submitted form being returned with the original data displayed, no validation errors displayed, no submitted data and no feedback as to why.  

The solution is to not redirect on validation failure, but render using the same instance of the form that failed the validation so the errors can be displayed.  

To this end I have moved all `context` setting to the top of the View before making any POST/GET pathing checks. In the event of a POST request the prefixes route the request to the correct Form handling in the View and form validation occurs (with the `.is_valid()` function). On failure the page is rendered again, but with the failed form replacing the initial form in the `context`.  

 We now create every form on every request, then override only the one that was submitted.  


## Custom validation in the Form  
We can override the `clean()` method on a Form. If we ensure to include `cleaned_data = super().clean()` at the start then what follows will simply add to the existing validation rather than replace it. Example `forms.py`:  

```python
class MyForm(forms.Form):
    id = forms.IntegerField()
    field= forms.CharField(label="Field", max_length=5)
    
    def clean(self):
        cleaned_data = super().clean()
        # 
        # do custom validation stuff on cleaned_data here
        # 
        return self.cleaned_data
```

It's possible to add `non_field_errors` that exist at the Form scope by including `None` in the field parameter of `.add_error()` like so:
```python
self.add_error(None, "Custom error message.")
```

These `non_field_errors` can be accessed from the template like so:
```html
{% if form.non_field_errors %}
    {% for error in form.non_field_errors %}
        {{error}}
    {% endfor %}
{% endif %}
```

If the form has been created in the template via Django's built in methods (e.g. `{{ form.as_p}}`) then any `non_field_errors` will be displayed at the top of the form automatically.  

Failure of these validation checks _will_ cause the submission to fail; _no_ changes to the database will be made. Any item added to `_errors` (as we have here) will cause `is_valid==False`.  


## Custom validation in the View  
Sometimes we may want to feedback on data issues without preventing submission of the data. For example, if there is a missing time period where contiguous time periods are expected it would be importnant to highlight that without preventing data being submitted that might partially resolve it as a step to completely resolving it!  

In these cases we can put validation checks in the GET request path of the View and pass them in to the context of the rendered page. This is acheived by adding an empty list in the context setting of the View and adding items to it in the custom validation of the View. I put them in the GET route because there's no benefit running them multiple times on a POST request. Example `views.py`:

```python
def MyView(request):
    custom_errors = []

    context = {'custom_errors': custom_errors}

    if request.method == 'GET':
        if validation_check_fails:
            custom_errors.append("Custom error message")

    return render(request, 'url.html', context)
```

As above, these `custom_errors` can be accessed from the template like so:
```html
{% if custom_errors %}
    {% for error in custom_errors %}
        {{error}}
    {% endfor %}
{% endif %}
```

Failure of these validation checks will _not_ cause the submission to fail; changes to the database _will_ be made. We're just passing through our own list of strings.    


## Validate initial data  
When creating the form with initial data, we may still want to validate the form.  

This `__init__` override will populate a temporary form (`temp`) with `data=initial` (as if it were a POST request) to trigger validation.  

Any errors are copied back in to the original form and displayed with the data from the database.  

```python
def __init__(self, *args, **kwargs): 
    super().__init__(*args, **kwargs)
    if self.initial: 
        temp = type(self)(data=self.initial) 
        if not temp.is_valid(): 
            self._errors = temp.errors
```