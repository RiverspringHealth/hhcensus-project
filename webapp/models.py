from django.db import models
import datetime
from django.utils import timezone
#from rest_framework import serializers
# Create your models here.
from django.db import models
from django.db.models import Lookup
from django.db.models.fields import Field
from unittest.util import _MAX_LENGTH
import os

from django.db import connection

from webapp import utilities
from hhcensus import settings

@Field.register_lookup
class NotEqual(Lookup):
    lookup_name = 'ne'

    def as_sql(self, qn, connection):
        lhs, lhs_params = self.process_lhs(qn, connection)
        rhs, rhs_params = self.process_rhs(qn, connection)
        params = lhs_params + rhs_params
        return '%s <> %s' % (lhs, rhs), params



def get_all_beds():
    with connection.cursor() as cursor:
        cursor.execute("SELECT UnitName+'-'+RoomAndBed [Bed] FROM dbo.mydataBed ORDER BY UnitName, RoomAndBed")
        rows = cursor.fetchall()
    return rows


INBED_CHOICES = (  ('',''),  #indicates not answered
                   ('Yes','Yes'),
                  ('No','No'),
                 
                )

REASON_CHOICES = (
            ("" ,""),
            ("Admission","Admission"),
            ("Discharge","Discharge"),
            ("Expiration","Expiration"),
            ("Out to Hospital","Out to Hospital"),
            ("Out to Leave of Absence","Out to Leave of Absence"),
            ("Return from Hospital","Return from Hospital"),
            ("Return from Leave of Absence","Return from Leave of Absence"),
            ("Room Change","Room Change"),
        )


        
class NightlyBedCheck(models.Model):
 #   id provided automatically by framework
    Unit = models.CharField(max_length=50, null=True, db_column='unit') #usually 2 #from PatientGroupAbbreviation
    Room = models.CharField(max_length=50) #actually room/bed to match legacy
    ResidentNumber = models.CharField(max_length=50, null=True)
    ResidentName = models.CharField(max_length=100, null=True)
    Status = models.CharField(max_length=50, null=True)
    LevelOfCare = models.CharField(max_length=50, null=True)
    Gender = models.CharField(max_length=50, null=True)
    CurrentAdmitDate = models.DateTimeField(null=True)
    Inbed = models.CharField(max_length=50, null=True, blank=True, default='',choices=INBED_CHOICES)
    Reason = models.CharField(max_length=300, null=True, blank=True, default='', choices=REASON_CHOICES)
    RepDate = models.DateField(null=True)
    Comments = models.CharField(max_length=300, null=True, blank=True, default='')    
    CreateDateTime = models.DateTimeField(auto_now_add=True)
    UpdatedByName = models.CharField(max_length=80, null=True, blank=True, default='', db_column='UpdateByName')
    UpdateDatetime =models.DateTimeField(null=True,  db_column='UpdateDatetime')
    Obsolete = models.IntegerField(default = 0)


    def __unicode__(self):
        return  self.__str__()

    def __str__(self):
        return str(( self.RepDate, self.Unit, self.Room, self.ResidentName, self.Inbed, self.Reason, self.Comments) )
        
    class Meta:
        db_table = 'NightlyBedCheck'
        managed = False
        
# class CensusActionType(models.Model):
#     Id = models.CharField(max_length=10, primary_key=True, null=False)
#     Description = models.CharField(max_length=80, null=False)
#     
#     def __unicode__(self):
#         return '{}={}'.format(self.Id, self.Description)
# 
#     def __str__(self):
#         return '{}={}'.format(self.id, self.description)
#         
#     class Meta:
#         pass
#         db_table = 'webapp_CensusActionType'
#         #managed = False
        



class CensusChangeLog(models.Model):
    action    = models.CharField(max_length=50, default='')
    firstname = models.CharField(max_length=50, default='')
    lastname  = models.CharField(max_length=50, default='')
    eventtime   = models.DateTimeField(null=True)
    oldbed      = models.CharField( max_length=10, default='')
    newbed      = models.CharField( max_length=10, default='')
    newloc      = models.CharField( max_length=20, default='')
    oldloc      = models.CharField( max_length=20, default='')
    admitfrom   = models.CharField(max_length=50, default='')
    dischargeto = models.CharField( max_length=50, default='')
    user        = models.CharField( max_length=50, default='')
    timestamp   = models.DateTimeField(auto_now_add=True, blank=True, null=True)
     
    class Meta:
        db_table = 'CensusChangeLog'
        managed = True   


