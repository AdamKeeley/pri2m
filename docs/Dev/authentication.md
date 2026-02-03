# Authentication using Entra ID

## Azure SQL Database  

Azure SQL Database: [Connect to MSSQL database in Django using Tokens](https://dev.to/kummerer94/connect-to-mssql-database-in-django-using-tokens-3oid)

Django can authenticate against the Azure SQL Database using tokens. 

In the dev environment Django authenticates against the database using whatever credential has been used in VSCode when running `az login`; _much_ more preferable than storing passwords!  

In production we should set up a User Managed Identity for the App resource to authenticate against the Database. This _should_ still work with `DefaultAzureCredential()` but we may need to look at chaining credentials.   

This authentication is at the app level and not the user logging in to the site.  

## User login and permissions  

Django Entra Auth: [django-entra-auth](https://pypi.org/project/django-entra-auth/)

`django-entra-auth` can be used to authenticate users against Entra ID and provides a `request.user.is_authenticated` status. It also pulls a bunch of user details from Entra ID and populates the Django user fields (eg `user`, `email` etc.).  

It requires an App Registration in Azure, with `User.Read` permissions on Microsoft Graph. In production we will need to use a key vault to store the `client_secret` of this App Registration.  

When logged in a user is created in Django Admin. Permissions for the site can be managed via Django Admin.  
[Using the Django authentication system](https://docs.djangoproject.com/en/6.0/topics/auth/default/)  

Decorators on views can be used to ensure they can only be accessed by authenticated users with the correct permissions.  

```python
@login_required
@permission_required("<app_label_>.<permission>_<model>", raise_exception=True)
def my_view():
    ...
```

There are four default permissions automatically created for every Model on migration:
- add: 'foo.add_bar'
- change: 'foo.change_bar'
- delete: 'foo.delete_bar'
- view: 'foo.view_bar'

We may need to make use of custom permissions moving forward but for now we'll make do with these.  

From Django Admin I have created a group and assigned permissions to the group. Adding users to the group assigns them those permissions. These permissions are checked by the above decorators and access denied if absent.  