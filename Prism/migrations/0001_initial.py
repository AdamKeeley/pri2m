# Generated by Django 5.0.14 on 2025-04-09 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tblproject',
            fields=[
                ('pid', models.IntegerField(db_column='pID', primary_key=True, serialize=False)),
                ('projectnumber', models.CharField(blank=True, db_column='ProjectNumber', max_length=5, null=True)),
                ('projectname', models.CharField(blank=True, db_column='ProjectName', max_length=500, null=True)),
                ('portfolionumber', models.CharField(blank=True, db_column='PortfolioNumber', max_length=255, null=True)),
                ('datrag', models.IntegerField(blank=True, db_column='DATRAG', null=True)),
                ('projectedstartdate', models.DateTimeField(blank=True, db_column='ProjectedStartDate', null=True)),
                ('projectedenddate', models.DateTimeField(blank=True, db_column='ProjectedEndDate', null=True)),
                ('startdate', models.DateTimeField(blank=True, db_column='StartDate', null=True)),
                ('enddate', models.DateTimeField(blank=True, db_column='EndDate', null=True)),
                ('pi', models.IntegerField(blank=True, db_column='PI', null=True)),
                ('leadapplicant', models.IntegerField(blank=True, db_column='LeadApplicant', null=True)),
                ('lida', models.BooleanField(blank=True, db_column='LIDA', null=True)),
                ('internship', models.BooleanField(blank=True, db_column='Internship', null=True)),
                ('dspt', models.BooleanField(blank=True, db_column='DSPT', null=True)),
                ('iso27001', models.BooleanField(blank=True, db_column='ISO27001', null=True)),
                ('laser', models.BooleanField(blank=True, db_column='LASER', null=True)),
                ('irc', models.BooleanField(blank=True, db_column='IRC', null=True)),
                ('seed', models.BooleanField(blank=True, db_column='SEED', null=True)),
                ('validfrom', models.DateTimeField(blank=True, db_column='ValidFrom', null=True)),
                ('validto', models.DateTimeField(blank=True, db_column='ValidTo', null=True)),
                ('createdby', models.CharField(blank=True, db_column='CreatedBy', max_length=50, null=True)),
            ],
            options={
                'db_table': 'tblProject',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tblprojectcostings',
            fields=[
                ('projectcostingsid', models.IntegerField(db_column='ProjectCostingsId', primary_key=True, serialize=False)),
                ('projectnumber', models.CharField(blank=True, db_column='ProjectNumber', max_length=5, null=True)),
                ('costingtypeid', models.IntegerField(blank=True, db_column='CostingTypeId', null=True)),
                ('datecosted', models.DateTimeField(blank=True, db_column='DateCosted', null=True)),
                ('fromdate', models.DateTimeField(blank=True, db_column='FromDate', null=True)),
                ('todate', models.DateTimeField(blank=True, db_column='ToDate', null=True)),
                ('duration', models.DecimalField(blank=True, db_column='Duration', decimal_places=1, max_digits=4, null=True)),
                ('durationcomputed', models.DecimalField(blank=True, db_column='DurationComputed', decimal_places=1, max_digits=4, null=True)),
                ('lasercompute', models.DecimalField(blank=True, db_column='LaserCompute', decimal_places=2, max_digits=19, null=True)),
                ('itssupport', models.DecimalField(blank=True, db_column='ItsSupport', decimal_places=2, max_digits=19, null=True)),
                ('fixedinfra', models.DecimalField(blank=True, db_column='FixedInfra', decimal_places=2, max_digits=19, null=True)),
                ('validfrom', models.DateTimeField(blank=True, db_column='ValidFrom', null=True)),
                ('validto', models.DateTimeField(blank=True, db_column='ValidTo', null=True)),
                ('createdby', models.CharField(blank=True, db_column='CreatedBy', max_length=12, null=True)),
            ],
            options={
                'db_table': 'tblProjectCostings',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tblprojectdatallocation',
            fields=[
                ('projectdatallocationid', models.IntegerField(db_column='ProjectDatAllocationId', primary_key=True, serialize=False)),
                ('projectnumber', models.CharField(blank=True, db_column='ProjectNumber', max_length=5, null=True)),
                ('fromdate', models.DateTimeField(blank=True, db_column='FromDate', null=True)),
                ('todate', models.DateTimeField(blank=True, db_column='ToDate', null=True)),
                ('duration', models.DecimalField(blank=True, db_column='Duration', decimal_places=1, max_digits=4, null=True)),
                ('durationcomputed', models.DecimalField(blank=True, db_column='DurationComputed', decimal_places=1, max_digits=4, null=True)),
                ('fte', models.DecimalField(blank=True, db_column='FTE', decimal_places=1, max_digits=4, null=True)),
                ('validfrom', models.DateTimeField(blank=True, db_column='ValidFrom', null=True)),
                ('validto', models.DateTimeField(blank=True, db_column='ValidTo', null=True)),
                ('createdby', models.CharField(blank=True, db_column='CreatedBy', max_length=12, null=True)),
            ],
            options={
                'db_table': 'tblProjectDatAllocation',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tblprojectdattime',
            fields=[
                ('dtid', models.IntegerField(db_column='dtID', primary_key=True, serialize=False)),
                ('projectnumber', models.CharField(blank=True, db_column='ProjectNumber', max_length=5, null=True)),
                ('dathours', models.DecimalField(blank=True, db_column='DatHours', decimal_places=1, max_digits=3, null=True)),
                ('created', models.DateTimeField(blank=True, db_column='Created', null=True)),
                ('createdby', models.CharField(blank=True, db_column='CreatedBy', max_length=50, null=True)),
            ],
            options={
                'db_table': 'tblProjectDatTime',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tblprojectdocument',
            fields=[
                ('pdid', models.IntegerField(db_column='pdID', primary_key=True, serialize=False)),
                ('projectnumber', models.CharField(blank=True, db_column='ProjectNumber', max_length=5, null=True)),
                ('versionnumber', models.DecimalField(blank=True, db_column='VersionNumber', decimal_places=2, max_digits=5, null=True)),
                ('submitted', models.DateTimeField(blank=True, db_column='Submitted', null=True)),
                ('accepted', models.DateTimeField(blank=True, db_column='Accepted', null=True)),
                ('validfrom', models.DateTimeField(blank=True, db_column='ValidFrom', null=True)),
                ('validto', models.DateTimeField(blank=True, db_column='ValidTo', null=True)),
                ('createdby', models.CharField(blank=True, db_column='CreatedBy', max_length=50, null=True)),
            ],
            options={
                'db_table': 'tblProjectDocument',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tblprojectkristal',
            fields=[
                ('projectkristalid', models.IntegerField(db_column='ProjectKristalID', primary_key=True, serialize=False)),
                ('projectnumber', models.CharField(blank=True, db_column='ProjectNumber', max_length=5, null=True)),
                ('kristalnumber', models.DecimalField(blank=True, db_column='KristalNumber', decimal_places=0, max_digits=6, null=True)),
                ('validfrom', models.DateTimeField(blank=True, db_column='ValidFrom', null=True)),
                ('validto', models.DateTimeField(blank=True, db_column='ValidTo', null=True)),
                ('createdby', models.CharField(blank=True, db_column='CreatedBy', max_length=50, null=True)),
            ],
            options={
                'db_table': 'tblProjectKristal',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tblprojectnotes',
            fields=[
                ('pnid', models.IntegerField(db_column='pnID', primary_key=True, serialize=False)),
                ('projectnumber', models.CharField(blank=True, db_column='ProjectNumber', max_length=5, null=True)),
                ('pnote', models.TextField(blank=True, db_column='pNote', null=True)),
                ('created', models.DateTimeField(blank=True, db_column='Created', null=True)),
                ('createdby', models.CharField(blank=True, db_column='CreatedBy', max_length=50, null=True)),
            ],
            options={
                'db_table': 'tblProjectNotes',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tblprojectplatforminfo',
            fields=[
                ('projectplatforminfoid', models.IntegerField(db_column='ProjectPlatformInfoID', primary_key=True, serialize=False)),
                ('projectnumber', models.CharField(blank=True, db_column='ProjectNumber', max_length=5, null=True)),
                ('projectplatforminfo', models.CharField(blank=True, db_column='ProjectPlatformInfo', max_length=255, null=True)),
                ('validfrom', models.DateTimeField(blank=True, db_column='ValidFrom', null=True)),
                ('validto', models.DateTimeField(blank=True, db_column='ValidTo', null=True)),
                ('createdby', models.CharField(blank=True, db_column='CreatedBy', max_length=50, null=True)),
                ('platforminfodescription', models.CharField(blank=True, db_column='PlatformInfoDescription', max_length=25, null=True)),
            ],
            options={
                'db_table': 'tblProjectPlatformInfo',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tbluser',
            fields=[
                ('userid', models.IntegerField(db_column='UserID', primary_key=True, serialize=False)),
                ('usernumber', models.IntegerField(blank=True, db_column='UserNumber', null=True)),
                ('firstname', models.CharField(blank=True, db_column='FirstName', max_length=50, null=True)),
                ('lastname', models.CharField(blank=True, db_column='LastName', max_length=50, null=True)),
                ('email', models.CharField(blank=True, db_column='Email', max_length=255, null=True)),
                ('phone', models.CharField(blank=True, db_column='Phone', max_length=15, null=True)),
                ('username', models.CharField(blank=True, db_column='UserName', max_length=12, null=True)),
                ('organisation', models.CharField(blank=True, db_column='Organisation', max_length=255, null=True)),
                ('startdate', models.DateTimeField(blank=True, db_column='StartDate', null=True)),
                ('enddate', models.DateTimeField(blank=True, db_column='EndDate', null=True)),
                ('priviledged', models.BooleanField(blank=True, db_column='Priviledged', null=True)),
                ('seedagreement', models.DateTimeField(blank=True, db_column='SEEDAgreement', null=True)),
                ('ircagreement', models.DateTimeField(blank=True, db_column='IRCAgreement', null=True)),
                ('laseragreement', models.DateTimeField(blank=True, db_column='LASERAgreement', null=True)),
                ('dataprotection', models.DateTimeField(blank=True, db_column='DataProtection', null=True)),
                ('informationsecurity', models.DateTimeField(blank=True, db_column='InformationSecurity', null=True)),
                ('iset', models.DateTimeField(blank=True, db_column='ISET', null=True)),
                ('isat', models.DateTimeField(blank=True, db_column='ISAT', null=True)),
                ('safe', models.DateTimeField(blank=True, db_column='SAFE', null=True)),
                ('tokenserial', models.BigIntegerField(blank=True, db_column='TokenSerial', null=True)),
                ('tokenissued', models.DateTimeField(blank=True, db_column='TokenIssued', null=True)),
                ('tokenreturned', models.DateTimeField(blank=True, db_column='TokenReturned', null=True)),
                ('validfrom', models.DateTimeField(blank=True, db_column='ValidFrom', null=True)),
                ('validto', models.DateTimeField(blank=True, db_column='ValidTo', null=True)),
                ('createdby', models.CharField(blank=True, db_column='CreatedBy', max_length=50, null=True)),
            ],
            options={
                'db_table': 'tblUser',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tlkclassification',
            fields=[
                ('classificationid', models.IntegerField(db_column='classificationID', primary_key=True, serialize=False)),
                ('classificationdescription', models.CharField(blank=True, db_column='classificationDescription', max_length=25, null=True)),
                ('validfrom', models.DateTimeField(blank=True, db_column='ValidFrom', null=True)),
                ('validto', models.DateTimeField(blank=True, db_column='ValidTo', null=True)),
            ],
            options={
                'db_table': 'tlkClassification',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tlkcostingtype',
            fields=[
                ('costingtypeid', models.IntegerField(db_column='CostingTypeId', primary_key=True, serialize=False)),
                ('costingtypedescription', models.CharField(blank=True, db_column='CostingTypeDescription', max_length=25, null=True)),
                ('validfrom', models.DateTimeField(blank=True, db_column='ValidFrom', null=True)),
                ('validto', models.DateTimeField(blank=True, db_column='ValidTo', null=True)),
                ('createdby', models.CharField(blank=True, db_column='CreatedBy', max_length=12, null=True)),
            ],
            options={
                'db_table': 'tlkCostingType',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tlkdocuments',
            fields=[
                ('documentid', models.IntegerField(db_column='DocumentID', primary_key=True, serialize=False)),
                ('documentdescription', models.CharField(blank=True, db_column='DocumentDescription', max_length=50, null=True)),
                ('validfrom', models.DateTimeField(blank=True, db_column='ValidFrom', null=True)),
                ('validto', models.DateTimeField(blank=True, db_column='ValidTo', null=True)),
            ],
            options={
                'db_table': 'tlkDocuments',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tlkfaculty',
            fields=[
                ('facultyid', models.IntegerField(db_column='facultyID', primary_key=True, serialize=False)),
                ('facultydescription', models.CharField(blank=True, db_column='facultyDescription', max_length=100, null=True)),
                ('validfrom', models.DateTimeField(blank=True, db_column='ValidFrom', null=True)),
                ('validto', models.DateTimeField(blank=True, db_column='ValidTo', null=True)),
            ],
            options={
                'db_table': 'tlkFaculty',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tlkplatforminfo',
            fields=[
                ('platforminfoid', models.IntegerField(db_column='PlatformInfoID', primary_key=True, serialize=False)),
                ('platforminfodescription', models.CharField(blank=True, db_column='PlatformInfoDescription', max_length=50, null=True)),
                ('validfrom', models.DateTimeField(blank=True, db_column='ValidFrom', null=True)),
                ('validto', models.DateTimeField(blank=True, db_column='ValidTo', null=True)),
            ],
            options={
                'db_table': 'tlkPlatformInfo',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tlkstage',
            fields=[
                ('stageid', models.IntegerField(db_column='StageID', primary_key=True, serialize=False)),
                ('pstagedescription', models.CharField(blank=True, db_column='pStageDescription', max_length=25, null=True)),
                ('stagenumber', models.DecimalField(blank=True, db_column='StageNumber', decimal_places=1, max_digits=3, null=True)),
                ('validfrom', models.DateTimeField(blank=True, db_column='ValidFrom', null=True)),
                ('validto', models.DateTimeField(blank=True, db_column='ValidTo', null=True)),
            ],
            options={
                'db_table': 'tlkStage',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tlktitle',
            fields=[
                ('titleid', models.IntegerField(db_column='TitleID', primary_key=True, serialize=False)),
                ('titledescription', models.CharField(blank=True, db_column='TitleDescription', max_length=25, null=True)),
                ('validfrom', models.DateTimeField(blank=True, db_column='ValidFrom', null=True)),
                ('validto', models.DateTimeField(blank=True, db_column='ValidTo', null=True)),
            ],
            options={
                'db_table': 'tlkTitle',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tlkuserstatus',
            fields=[
                ('statusid', models.IntegerField(db_column='StatusID', primary_key=True, serialize=False)),
                ('statusdescription', models.CharField(blank=True, db_column='StatusDescription', max_length=25, null=True)),
                ('validfrom', models.DateTimeField(blank=True, db_column='ValidFrom', null=True)),
                ('validto', models.DateTimeField(blank=True, db_column='ValidTo', null=True)),
            ],
            options={
                'db_table': 'tlkUserStatus',
                'managed': False,
            },
        ),
    ]
