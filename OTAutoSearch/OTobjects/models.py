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

class Comments(models.Model):
    OTid = models.ForeignKey(OTuniq,db_column='OTid')
    comment = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'comments'
        ordering = ['OTid']
    def  __unicode__(self):
        return str(self.OTid)
