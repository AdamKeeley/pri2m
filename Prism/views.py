from django.shortcuts import render
from django.apps import apps
import pyodbc

def connection():
    s = 'adam-playground.database.windows.net'
    d = 'playground' 
    u = 'django'
    p = 'SuperSecurePassword321'
    cstr = 'DRIVER={ODBC Driver 18 for SQL Server};SERVER='+s+';DATABASE='+d+';UID='+u+';PWD='+ p
    conn = pyodbc.connect(cstr)
    return conn

def projects(request):
    projects = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT top (5) pID, ProjectNumber, ProjectName, Stage, PI, Faculty FROM dbo.tblProject where ValidTo is null")
    for row in cursor.fetchall():
        projects.append({"pID": row[0], "ProjectNumber": row[1], "ProjectName": row[2], "Stage": row[3], "PI": row[4], "Faculty": row[5]})
    conn.close()
    return render(request, 'projects.html', {'projects':projects})