---
layout: default
title: Django initiation
nav_order: 1
has_children: false
---

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