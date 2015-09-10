# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'OTuniq'
        db.create_table('otuniq', (
            ('OTid', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_index=True)),
            ('x', self.gf('django.db.models.fields.FloatField')()),
            ('y', self.gf('django.db.models.fields.FloatField')()),
            ('Ra', self.gf('django.db.models.fields.FloatField')()),
            ('Dec', self.gf('django.db.models.fields.FloatField')()),
            ('magcalib', self.gf('django.db.models.fields.FloatField')()),
            ('magres', self.gf('django.db.models.fields.FloatField')()),
            ('magErr', self.gf('django.db.models.fields.FloatField')()),
            ('magorig', self.gf('django.db.models.fields.FloatField')()),
            ('magorigErr', self.gf('django.db.models.fields.FloatField')()),
            ('magref', self.gf('django.db.models.fields.FloatField')()),
            ('magrefErr', self.gf('django.db.models.fields.FloatField')()),
            ('counts', self.gf('django.db.models.fields.IntegerField')()),
            ('c_filter', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'OTobjects', ['OTuniq'])

        # Adding model 'Catfiles'
        db.create_table('catfiles', (
            ('Catid', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_index=True)),
            ('Catna', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('orig_im', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('ref_im', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('JD', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'OTobjects', ['Catfiles'])

        # Adding model 'OTcands'
        db.create_table('otcands', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('OTid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['OTobjects.OTuniq'], db_column='OTid')),
            ('Catid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['OTobjects.Catfiles'], db_column='Catid')),
            ('x', self.gf('django.db.models.fields.FloatField')()),
            ('y', self.gf('django.db.models.fields.FloatField')()),
            ('Ra', self.gf('django.db.models.fields.FloatField')()),
            ('Dec', self.gf('django.db.models.fields.FloatField')()),
            ('magres', self.gf('django.db.models.fields.FloatField')()),
            ('magresErr', self.gf('django.db.models.fields.FloatField')()),
            ('magorig', self.gf('django.db.models.fields.FloatField')()),
            ('magorigErr', self.gf('django.db.models.fields.FloatField')()),
            ('magrescalib', self.gf('django.db.models.fields.FloatField')()),
            ('filter', self.gf('django.db.models.fields.IntegerField')(max_length=1)),
            ('tag_refstr', self.gf('django.db.models.fields.IntegerField')(max_length=1)),
        ))
        db.send_create_signal(u'OTobjects', ['OTcands'])

        # Adding model 'Fchart'
        db.create_table('fchart', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('OTid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['OTobjects.OTuniq'], db_column='OTid')),
            ('Catid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['OTobjects.Catfiles'], db_column='Catid')),
            ('Fname', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('Fpath', self.gf('django.db.models.fields.CharField')(default='/home/madong/projects/django/OTAutoSearch/OTobjects/static/OTobjects', max_length=100)),
        ))
        db.send_create_signal(u'OTobjects', ['Fchart'])


    def backwards(self, orm):
        # Deleting model 'OTuniq'
        db.delete_table('otuniq')

        # Deleting model 'Catfiles'
        db.delete_table('catfiles')

        # Deleting model 'OTcands'
        db.delete_table('otcands')

        # Deleting model 'Fchart'
        db.delete_table('fchart')


    models = {
        u'OTobjects.catfiles': {
            'Catid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_index': 'True'}),
            'Catna': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'JD': ('django.db.models.fields.FloatField', [], {}),
            'Meta': {'ordering': "['Catid']", 'object_name': 'Catfiles', 'db_table': "'catfiles'"},
            'orig_im': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'ref_im': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'OTobjects.fchart': {
            'Catid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['OTobjects.Catfiles']", 'db_column': "'Catid'"}),
            'Fname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'Fpath': ('django.db.models.fields.CharField', [], {'default': "'/home/madong/projects/django/OTAutoSearch/OTobjects/static/OTobjects'", 'max_length': '100'}),
            'Meta': {'ordering': "['OTid', 'Catid']", 'object_name': 'Fchart', 'db_table': "'fchart'"},
            'OTid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['OTobjects.OTuniq']", 'db_column': "'OTid'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'OTobjects.otcands': {
            'Catid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['OTobjects.Catfiles']", 'db_column': "'Catid'"}),
            'Dec': ('django.db.models.fields.FloatField', [], {}),
            'Meta': {'ordering': "['OTid', 'Catid']", 'object_name': 'OTcands', 'db_table': "'otcands'"},
            'OTid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['OTobjects.OTuniq']", 'db_column': "'OTid'"}),
            'Ra': ('django.db.models.fields.FloatField', [], {}),
            'filter': ('django.db.models.fields.IntegerField', [], {'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'magorig': ('django.db.models.fields.FloatField', [], {}),
            'magorigErr': ('django.db.models.fields.FloatField', [], {}),
            'magres': ('django.db.models.fields.FloatField', [], {}),
            'magresErr': ('django.db.models.fields.FloatField', [], {}),
            'magrescalib': ('django.db.models.fields.FloatField', [], {}),
            'tag_refstr': ('django.db.models.fields.IntegerField', [], {'max_length': '1'}),
            'x': ('django.db.models.fields.FloatField', [], {}),
            'y': ('django.db.models.fields.FloatField', [], {})
        },
        u'OTobjects.otuniq': {
            'Dec': ('django.db.models.fields.FloatField', [], {}),
            'Meta': {'ordering': "['OTid']", 'object_name': 'OTuniq', 'db_table': "'otuniq'"},
            'OTid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_index': 'True'}),
            'Ra': ('django.db.models.fields.FloatField', [], {}),
            'c_filter': ('django.db.models.fields.FloatField', [], {}),
            'counts': ('django.db.models.fields.IntegerField', [], {}),
            'magErr': ('django.db.models.fields.FloatField', [], {}),
            'magcalib': ('django.db.models.fields.FloatField', [], {}),
            'magorig': ('django.db.models.fields.FloatField', [], {}),
            'magorigErr': ('django.db.models.fields.FloatField', [], {}),
            'magref': ('django.db.models.fields.FloatField', [], {}),
            'magrefErr': ('django.db.models.fields.FloatField', [], {}),
            'magres': ('django.db.models.fields.FloatField', [], {}),
            'x': ('django.db.models.fields.FloatField', [], {}),
            'y': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['OTobjects']