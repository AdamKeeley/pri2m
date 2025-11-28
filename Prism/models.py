# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Tblproject(models.Model):
    pid = models.AutoField(db_column='pID', primary_key=True, editable=False)  # Field name made lowercase.
    projectnumber = models.CharField(db_column='ProjectNumber', max_length=5, blank=True, null=True)  # Field name made lowercase.
    projectname = models.CharField(db_column='ProjectName', max_length=500, blank=True, null=True)  # Field name made lowercase.
    portfolionumber = models.CharField(db_column='PortfolioNumber', max_length=255, blank=True, null=True)  # Field name made lowercase.
    stage = models.ForeignKey('Tlkstage', models.PROTECT, db_column='Stage', blank=True, null=True)  # Field name made lowercase.
    classification = models.ForeignKey('Tlkclassification', models.PROTECT, db_column='Classification', blank=True, null=True)  # Field name made lowercase.
    datrag = models.IntegerField(db_column='DATRAG', blank=True, null=True)  # Field name made lowercase.
    projectedstartdate = models.DateTimeField(db_column='ProjectedStartDate', blank=True, null=True)  # Field name made lowercase.
    projectedenddate = models.DateTimeField(db_column='ProjectedEndDate', blank=True, null=True)  # Field name made lowercase.
    startdate = models.DateTimeField(db_column='StartDate', blank=True, null=True)  # Field name made lowercase.
    enddate = models.DateTimeField(db_column='EndDate', blank=True, null=True)  # Field name made lowercase.
    pi = models.IntegerField(db_column='PI', blank=True, null=True)  # Field name made lowercase.
    leadapplicant = models.IntegerField(db_column='LeadApplicant', blank=True, null=True)  # Field name made lowercase.
    faculty = models.ForeignKey('Tlkfaculty', models.PROTECT, db_column='Faculty', blank=True, null=True)  # Field name made lowercase.
    lida = models.BooleanField(db_column='LIDA', blank=True, null=True)  # Field name made lowercase.
    internship = models.BooleanField(db_column='Internship', blank=True, null=True)  # Field name made lowercase.
    dspt = models.BooleanField(db_column='DSPT', blank=True, null=True)  # Field name made lowercase.
    iso27001 = models.BooleanField(db_column='ISO27001', blank=True, null=True)  # Field name made lowercase.
    laser = models.BooleanField(db_column='LASER', blank=True, null=True)  # Field name made lowercase.
    irc = models.BooleanField(db_column='IRC', blank=True, null=True)  # Field name made lowercase.
    seed = models.BooleanField(db_column='SEED', blank=True, null=True)  # Field name made lowercase.
    validfrom = models.DateTimeField(db_column='ValidFrom', blank=True, null=True)  # Field name made lowercase.
    validto = models.DateTimeField(db_column='ValidTo', blank=True, null=True)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tblProject'


class Tblprojectcostings(models.Model):
    projectcostingsid = models.IntegerField(db_column='ProjectCostingsId', primary_key=True)  # Field name made lowercase.
    projectnumber = models.CharField(db_column='ProjectNumber', max_length=5, blank=True, null=True)  # Field name made lowercase.
    costingtypeid = models.IntegerField(db_column='CostingTypeId', blank=True, null=True)  # Field name made lowercase.
    datecosted = models.DateTimeField(db_column='DateCosted', blank=True, null=True)  # Field name made lowercase.
    fromdate = models.DateTimeField(db_column='FromDate', blank=True, null=True)  # Field name made lowercase.
    todate = models.DateTimeField(db_column='ToDate', blank=True, null=True)  # Field name made lowercase.
    duration = models.DecimalField(db_column='Duration', max_digits=4, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    durationcomputed = models.DecimalField(db_column='DurationComputed', max_digits=4, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    lasercompute = models.DecimalField(db_column='LaserCompute', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    itssupport = models.DecimalField(db_column='ItsSupport', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    fixedinfra = models.DecimalField(db_column='FixedInfra', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    validfrom = models.DateTimeField(db_column='ValidFrom', blank=True, null=True)  # Field name made lowercase.
    validto = models.DateTimeField(db_column='ValidTo', blank=True, null=True)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tblProjectCostings'


class Tblprojectdatallocation(models.Model):
    projectdatallocationid = models.IntegerField(db_column='ProjectDatAllocationId', primary_key=True)  # Field name made lowercase.
    projectnumber = models.CharField(db_column='ProjectNumber', max_length=5, blank=True, null=True)  # Field name made lowercase.
    fromdate = models.DateTimeField(db_column='FromDate', blank=True, null=True)  # Field name made lowercase.
    todate = models.DateTimeField(db_column='ToDate', blank=True, null=True)  # Field name made lowercase.
    duration = models.DecimalField(db_column='Duration', max_digits=4, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    durationcomputed = models.DecimalField(db_column='DurationComputed', max_digits=4, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    fte = models.DecimalField(db_column='FTE', max_digits=4, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    validfrom = models.DateTimeField(db_column='ValidFrom', blank=True, null=True)  # Field name made lowercase.
    validto = models.DateTimeField(db_column='ValidTo', blank=True, null=True)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tblProjectDatAllocation'


class Tblprojectdattime(models.Model):
    dtid = models.IntegerField(db_column='dtID', primary_key=True)  # Field name made lowercase.
    projectnumber = models.CharField(db_column='ProjectNumber', max_length=5, blank=True, null=True)  # Field name made lowercase.
    dathours = models.DecimalField(db_column='DatHours', max_digits=3, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    created = models.DateTimeField(db_column='Created', blank=True, null=True)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tblProjectDatTime'


class Tblprojectdocument(models.Model):
    pdid = models.AutoField(db_column='pdID', primary_key=True, editable=False)  # Field name made lowercase.
    projectnumber = models.CharField(db_column='ProjectNumber', max_length=5, blank=True, null=True)  # Field name made lowercase.
    documenttype = models.ForeignKey('Tlkdocuments', models.PROTECT, db_column='DocumentType', blank=True, null=True)  # Field name made lowercase.
    versionnumber = models.DecimalField(db_column='VersionNumber', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    submitted = models.DateTimeField(db_column='Submitted', blank=True, null=True)  # Field name made lowercase.
    accepted = models.DateTimeField(db_column='Accepted', blank=True, null=True)  # Field name made lowercase.
    validfrom = models.DateTimeField(db_column='ValidFrom', blank=True, null=True)  # Field name made lowercase.
    validto = models.DateTimeField(db_column='ValidTo', blank=True, null=True)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tblProjectDocument'


class Tblprojectkristal(models.Model):
    projectkristalid = models.IntegerField(db_column='ProjectKristalID', primary_key=True)  # Field name made lowercase.
    projectnumber = models.CharField(db_column='ProjectNumber', max_length=5, blank=True, null=True)  # Field name made lowercase.
    kristalnumber = models.DecimalField(db_column='KristalNumber', max_digits=6, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    validfrom = models.DateTimeField(db_column='ValidFrom', blank=True, null=True)  # Field name made lowercase.
    validto = models.DateTimeField(db_column='ValidTo', blank=True, null=True)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tblProjectKristal'


class Tblprojectnotes(models.Model):
    pnid = models.AutoField(db_column='pnID', primary_key=True, editable=False)
    projectnumber = models.CharField(db_column='ProjectNumber', max_length=5, blank=True, null=True)  # Field name made lowercase.
    pnote = models.TextField(db_column='pNote', blank=True, null=True)  # Field name made lowercase.
    created = models.DateTimeField(db_column='Created', blank=True, null=True)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tblProjectNotes'


class Tblprojectplatforminfo(models.Model):
    projectplatforminfoid = models.IntegerField(db_column='ProjectPlatformInfoID', primary_key=True)  # Field name made lowercase.
    projectnumber = models.CharField(db_column='ProjectNumber', max_length=5, blank=True, null=True)  # Field name made lowercase.
    platforminfoid = models.ForeignKey('Tlkplatforminfo', models.PROTECT, db_column='PlatformInfoID', blank=True, null=True)  # Field name made lowercase.
    projectplatforminfo = models.CharField(db_column='ProjectPlatformInfo', max_length=255, blank=True, null=True)  # Field name made lowercase.
    validfrom = models.DateTimeField(db_column='ValidFrom', blank=True, null=True)  # Field name made lowercase.
    validto = models.DateTimeField(db_column='ValidTo', blank=True, null=True)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=50, blank=True, null=True)  # Field name made lowercase.
    platforminfodescription = models.CharField(db_column='PlatformInfoDescription', max_length=25, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tblProjectPlatformInfo'


class Tbluser(models.Model):
    userid = models.IntegerField(db_column='UserID', primary_key=True)  # Field name made lowercase.
    usernumber = models.IntegerField(db_column='UserNumber', blank=True, null=True)  # Field name made lowercase.
    status = models.ForeignKey('Tlkuserstatus', models.PROTECT, db_column='Status', blank=True, null=True)  # Field name made lowercase.
    title = models.ForeignKey('Tlktitle', models.PROTECT, db_column='Title', blank=True, null=True)  # Field name made lowercase.
    firstname = models.CharField(db_column='FirstName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    lastname = models.CharField(db_column='LastName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=255, blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', max_length=15, blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(db_column='UserName', max_length=12, blank=True, null=True)  # Field name made lowercase.
    organisation = models.CharField(db_column='Organisation', max_length=255, blank=True, null=True)  # Field name made lowercase.
    startdate = models.DateTimeField(db_column='StartDate', blank=True, null=True)  # Field name made lowercase.
    enddate = models.DateTimeField(db_column='EndDate', blank=True, null=True)  # Field name made lowercase.
    priviledged = models.BooleanField(db_column='Priviledged', blank=True, null=True)  # Field name made lowercase.
    seedagreement = models.DateTimeField(db_column='SEEDAgreement', blank=True, null=True)  # Field name made lowercase.
    ircagreement = models.DateTimeField(db_column='IRCAgreement', blank=True, null=True)  # Field name made lowercase.
    laseragreement = models.DateTimeField(db_column='LASERAgreement', blank=True, null=True)  # Field name made lowercase.
    dataprotection = models.DateTimeField(db_column='DataProtection', blank=True, null=True)  # Field name made lowercase.
    informationsecurity = models.DateTimeField(db_column='InformationSecurity', blank=True, null=True)  # Field name made lowercase.
    iset = models.DateTimeField(db_column='ISET', blank=True, null=True)  # Field name made lowercase.
    isat = models.DateTimeField(db_column='ISAT', blank=True, null=True)  # Field name made lowercase.
    safe = models.DateTimeField(db_column='SAFE', blank=True, null=True)  # Field name made lowercase.
    tokenserial = models.BigIntegerField(db_column='TokenSerial', blank=True, null=True)  # Field name made lowercase.
    tokenissued = models.DateTimeField(db_column='TokenIssued', blank=True, null=True)  # Field name made lowercase.
    tokenreturned = models.DateTimeField(db_column='TokenReturned', blank=True, null=True)  # Field name made lowercase.
    validfrom = models.DateTimeField(db_column='ValidFrom', blank=True, null=True)  # Field name made lowercase.
    validto = models.DateTimeField(db_column='ValidTo', blank=True, null=True)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=50, blank=True, null=True)  # Field name made lowercase.

    @property
    def full_name(self):
        "Returns the user's full name."
        return f"{self.firstname} {self.lastname}"

    def __str__(self):
        return f"{self.firstname} {self.lastname}"
    
    class Meta:
        managed = False
        db_table = 'tblUser'


class Tlkclassification(models.Model):
    classificationid = models.IntegerField(db_column='classificationID', primary_key=True)  # Field name made lowercase.
    classificationdescription = models.CharField(db_column='classificationDescription', max_length=25, blank=True, null=True)  # Field name made lowercase.
    validfrom = models.DateTimeField(db_column='ValidFrom', blank=True, null=True)  # Field name made lowercase.
    validto = models.DateTimeField(db_column='ValidTo', blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.classificationdescription

    class Meta:
        managed = False
        db_table = 'tlkClassification'


class Tlkcostingtype(models.Model):
    costingtypeid = models.IntegerField(db_column='CostingTypeId', primary_key=True)  # Field name made lowercase.
    costingtypedescription = models.CharField(db_column='CostingTypeDescription', max_length=25, blank=True, null=True)  # Field name made lowercase.
    validfrom = models.DateTimeField(db_column='ValidFrom', blank=True, null=True)  # Field name made lowercase.
    validto = models.DateTimeField(db_column='ValidTo', blank=True, null=True)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=12, blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.costingtypedescription

    class Meta:
        managed = False
        db_table = 'tlkCostingType'


class Tlkdocuments(models.Model):
    documentid = models.IntegerField(db_column='DocumentID', primary_key=True)  # Field name made lowercase.
    documentdescription = models.CharField(db_column='DocumentDescription', max_length=50, blank=True, null=True)  # Field name made lowercase.
    validfrom = models.DateTimeField(db_column='ValidFrom', blank=True, null=True)  # Field name made lowercase.
    validto = models.DateTimeField(db_column='ValidTo', blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.documentdescription
    
    class Meta:
        managed = False
        db_table = 'tlkDocuments'


class Tlkfaculty(models.Model):
    facultyid = models.IntegerField(db_column='facultyID', primary_key=True)  # Field name made lowercase.
    facultydescription = models.CharField(db_column='facultyDescription', max_length=100, blank=True, null=True)  # Field name made lowercase.
    validfrom = models.DateTimeField(db_column='ValidFrom', blank=True, null=True)  # Field name made lowercase.
    validto = models.DateTimeField(db_column='ValidTo', blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.facultydescription

    class Meta:
        managed = False
        db_table = 'tlkFaculty'


class Tlkplatforminfo(models.Model):
    platforminfoid = models.IntegerField(db_column='PlatformInfoID', primary_key=True)  # Field name made lowercase.
    platforminfodescription = models.CharField(db_column='PlatformInfoDescription', max_length=50, blank=True, null=True)  # Field name made lowercase.
    validfrom = models.DateTimeField(db_column='ValidFrom', blank=True, null=True)  # Field name made lowercase.
    validto = models.DateTimeField(db_column='ValidTo', blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.platforminfodescription

    class Meta:
        managed = False
        db_table = 'tlkPlatformInfo'


class Tlkstage(models.Model):
    stageid = models.IntegerField(db_column='StageID', primary_key=True)  # Field name made lowercase.
    pstagedescription = models.CharField(db_column='pStageDescription', max_length=25, blank=True, null=True)  # Field name made lowercase.
    stagenumber = models.DecimalField(db_column='StageNumber', max_digits=3, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    validfrom = models.DateTimeField(db_column='ValidFrom', blank=True, null=True)  # Field name made lowercase.
    validto = models.DateTimeField(db_column='ValidTo', blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.pstagedescription

    class Meta:
        managed = False
        db_table = 'tlkStage'


class Tlktitle(models.Model):
    titleid = models.IntegerField(db_column='TitleID', primary_key=True)  # Field name made lowercase.
    titledescription = models.CharField(db_column='TitleDescription', max_length=25, blank=True, null=True)  # Field name made lowercase.
    validfrom = models.DateTimeField(db_column='ValidFrom', blank=True, null=True)  # Field name made lowercase.
    validto = models.DateTimeField(db_column='ValidTo', blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.titledescription

    class Meta:
        managed = False
        db_table = 'tlkTitle'


class Tlkuserstatus(models.Model):
    statusid = models.IntegerField(db_column='StatusID', primary_key=True)  # Field name made lowercase.
    statusdescription = models.CharField(db_column='StatusDescription', max_length=25, blank=True, null=True)  # Field name made lowercase.
    validfrom = models.DateTimeField(db_column='ValidFrom', blank=True, null=True)  # Field name made lowercase.
    validto = models.DateTimeField(db_column='ValidTo', blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.statusdescription

    class Meta:
        managed = False
        db_table = 'tlkUserStatus'
