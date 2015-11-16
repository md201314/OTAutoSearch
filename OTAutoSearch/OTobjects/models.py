from django.db import models
import os
from OTAutoSearch.settings import base_path,static_path

Fchart_path = os.path.join(static_path,'OTobjects/Fchart')
# Create your models here.
class OTuniq(models.Model):
    STATUS_CHOICES = ((-1,'False transient'),(0,'To be confirmed'),(1,'True transient'),(2,'Continue to be confirmed'),)
    OTid = models.AutoField(primary_key=True,db_index=True)
    x = models.FloatField()
    y = models.FloatField()
    Ra = models.FloatField()
    Dec = models.FloatField()
    skyid = models.CharField(max_length=6,db_index=True)
    magcalib = models.FloatField()
    magres = models.FloatField()
    magErr = models.FloatField()
    magorig = models.FloatField()
    magorigErr = models.FloatField()
    magref = models.FloatField()
    magrefErr = models.FloatField()
    counts = models.IntegerField(default=1)
    c_filter = models.FloatField()
    status = models.IntegerField(max_length=1,choices=STATUS_CHOICES,default=0)

    class Meta:
        db_table = 'otuniq'
        ordering = ['OTid']
    def __unicode__(self):
        return str(self.OTid)

class Catfiles(models.Model):
    Catid = models.AutoField(primary_key=True,db_index=True)
    Catna = models.CharField(max_length=50,unique=True)
    orig_im = models.CharField(max_length=50)
    ref_im = models.CharField(max_length=50)
    JD = models.FloatField()
    mountid = models.CharField(max_length=2)
    cameraid = models.CharField(max_length=2)
    ymd = models.CharField(max_length=6)
    skyid = models.CharField(max_length=6)
    mcysids = models.CharField(max_length=19)

    class Meta:
        db_table = 'catfiles'
        ordering = ['Catid']
    def __unicode__(self):
        return str(self.Catid)

class OTcands(models.Model):
    OTid = models.ForeignKey(OTuniq,db_column='OTid')
    Catid = models.ForeignKey(Catfiles,db_column='Catid')
    x = models.FloatField()
    y = models.FloatField()
    Ra = models.FloatField()
    Dec = models.FloatField()
    magres = models.FloatField()
    magresErr = models.FloatField()
    magorig = models.FloatField()
    magorigErr = models.FloatField()
    magrescalib = models.FloatField()
    filter = models.IntegerField(max_length=1)
    tag_refstr = models.IntegerField(max_length=1)

    class Meta:
        db_table = 'otcands'
        ordering = ['OTid','Catid']
    def __unicode__(self):
        return str(self.OTid)

class Fchart(models.Model):
    OTid = models.ForeignKey(OTuniq,db_column='OTid')
    Catid = models.ForeignKey(Catfiles,db_column='Catid')
    Fname = models.CharField(max_length=50,unique=True)
    Fpath = models.CharField(max_length=100,default=Fchart_path)

    class Meta:
        db_table = 'fchart'
        ordering = ['OTid','Catid']
    def __unicode__(self):
        return str(self.OTid)

class Users(models.Model):
    uid = models.AutoField(primary_key=True,db_index=True)
    uname = models.CharField(max_length=16,unique=True,db_index=True)
    passwd = models.CharField(max_length=50)
    email_add = models.EmailField()
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30)
    status = models.NullBooleanField(default=False)
    
    class Meta:
        db_table = 'users'
        ordering = ['uid']
    def __unicode__(self):
        return str(self.uid)

class Comments(models.Model):
    STATUS_CHOICES = ((-1,'False transient'),(0,'To be confirmed'),(1,'True transient'),(2,'Continue to be confirmed'),)
    OTid = models.ForeignKey(OTuniq,db_column='OTid')
    uid = models.ForeignKey(Users,db_column='uid')
    status = status = models.IntegerField(max_length=1,choices=STATUS_CHOICES,default=0)
    comment = models.TextField(blank=True)
    datetime = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'comments'
        ordering = ['OTid']
    def  __unicode__(self):
        return str(self.OTid)

