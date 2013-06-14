# -*- coding: utf-8 -*-
# flake8: noqa
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EmailSubscriber'
        db.create_table(u'tinyblog_emailsubscriber', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('subscribed', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('confirmed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('unsubscribed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('uuid_first', self.gf('uuidfield.fields.UUIDField')(unique=True, max_length=32, blank=True)),
            ('uuid_second', self.gf('uuidfield.fields.UUIDField')(unique=True, max_length=32, blank=True)),
        ))
        db.send_create_signal(u'tinyblog', ['EmailSubscriber'])

        # Adding model 'Post'
        db.create_table(u'tinyblog_post', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('teaser_html', self.gf('django.db.models.fields.TextField')()),
            ('text_html', self.gf('django.db.models.fields.TextField')()),
            ('emailed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'tinyblog', ['Post'])


    def backwards(self, orm):
        # Deleting model 'EmailSubscriber'
        db.delete_table(u'tinyblog_emailsubscriber')

        # Deleting model 'Post'
        db.delete_table(u'tinyblog_post')


    models = {
        u'tinyblog.emailsubscriber': {
            'Meta': {'object_name': 'EmailSubscriber'},
            'confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subscribed': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'unsubscribed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'uuid_first': ('uuidfield.fields.UUIDField', [], {'unique': 'True', 'max_length': '32', 'blank': 'True'}),
            'uuid_second': ('uuidfield.fields.UUIDField', [], {'unique': 'True', 'max_length': '32', 'blank': 'True'})
        },
        u'tinyblog.post': {
            'Meta': {'ordering': "['-created']", 'object_name': 'Post'},
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'emailed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'teaser_html': ('django.db.models.fields.TextField', [], {}),
            'text_html': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['tinyblog']
