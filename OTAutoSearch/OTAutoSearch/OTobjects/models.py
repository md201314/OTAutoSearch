from django.db import models

# Create your models here.
class OTuniq(models.Model):
    OTid = models.AutoField(primary_key=True,db_index=True)
    x = models.FloatField()
    y = models.FloatField()
    Ra = models.FloatField()
    Dec = models.FloatField()
    magcalib = models.FloatField()
    magErr = models.FloatField()
    magres = models.FloatField()
    magorig = models.FloatField()
    magorigErr = models.FloatField()
    counts = models.FloatField()
    c_filter = models.FloatField()

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
    magrescalib = models.FloatField()
    filter = models.IntegerField(max_length=1)
    tag_refstr = models.IntegerField(max_length=1)

    class Meta:
        db_table = 'otcands'
        ordering = ['OTid','Catid']
    def __unicode__(self):
        return str(self.OTid)
