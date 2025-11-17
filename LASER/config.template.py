server = ''
database = ''
user = ''
password = ''

DATABASE = {
    'default': {
        'ENGINE': 'mssql',
        'HOST': server,
        'NAME': database,
        'USER': user,
        'PASSWORD': password,
        'PORT': '',
        'OPTIONS': {
            'driver': 'ODBC Driver 18 for SQL Server',
            #"extra_params": "Authentication=ActiveDirectoryInteractive",
        }
    }
}