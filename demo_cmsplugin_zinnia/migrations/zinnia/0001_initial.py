"""
Initial migration for Zinnia v0.14.2
"""
from south.db import db
from south.v2 import SchemaMigration
from south.utils import datetime_utils as datetime

from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Entry'
        db.create_table(u'zinnia_entry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=0, db_index=True)),
            ('start_publication', self.gf('django.db.models.fields.DateTimeField')(db_index=True, null=True, blank=True)),
            ('end_publication', self.gf('django.db.models.fields.DateTimeField')(db_index=True, null=True, blank=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, db_index=True)),
            ('last_update', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('comment_enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('pingback_enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('trackback_enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('comment_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('pingback_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('trackback_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('excerpt', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('featured', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('tags', self.gf('tagging.fields.TagField')()),
            ('login_required', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('content_template', self.gf('django.db.models.fields.CharField')(default='zinnia/_entry_detail.html', max_length=250)),
            ('detail_template', self.gf('django.db.models.fields.CharField')(default='entry_detail.html', max_length=250)),
        ))
        db.send_create_signal('zinnia', ['Entry'])

        # Adding index on 'Entry', fields ['slug', 'creation_date']
        db.create_index(u'zinnia_entry', ['slug', 'creation_date'])

        # Adding index on 'Entry', fields ['status', 'creation_date', 'start_publication', 'end_publication']
        db.create_index(u'zinnia_entry', ['status', 'creation_date', 'start_publication', 'end_publication'])

        # Adding M2M table for field sites on 'Entry'
        m2m_table_name = db.shorten_name(u'zinnia_entry_sites')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('entry', models.ForeignKey(orm['zinnia.entry'], null=False)),
            ('site', models.ForeignKey(orm[u'sites.site'], null=False))
        ))
        db.create_unique(m2m_table_name, ['entry_id', 'site_id'])

        # Adding M2M table for field related on 'Entry'
        m2m_table_name = db.shorten_name(u'zinnia_entry_related')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_entry', models.ForeignKey(orm['zinnia.entry'], null=False)),
            ('to_entry', models.ForeignKey(orm['zinnia.entry'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_entry_id', 'to_entry_id'])

        # Adding M2M table for field authors on 'Entry'
        m2m_table_name = db.shorten_name(u'zinnia_entry_authors')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('entry', models.ForeignKey(orm['zinnia.entry'], null=False)),
            ('author', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['entry_id', 'author_id'])

        # Adding M2M table for field categories on 'Entry'
        m2m_table_name = db.shorten_name(u'zinnia_entry_categories')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('entry', models.ForeignKey(orm['zinnia.entry'], null=False)),
            ('category', models.ForeignKey(orm['zinnia.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['entry_id', 'category_id'])

        # Adding model 'Category'
        db.create_table(u'zinnia_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['zinnia.Category'])),
            (u'lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('zinnia', ['Category'])


    def backwards(self, orm):
        # Removing index on 'Entry', fields ['status', 'creation_date', 'start_publication', 'end_publication']
        db.delete_index(u'zinnia_entry', ['status', 'creation_date', 'start_publication', 'end_publication'])

        # Removing index on 'Entry', fields ['slug', 'creation_date']
        db.delete_index(u'zinnia_entry', ['slug', 'creation_date'])

        # Deleting model 'Entry'
        db.delete_table(u'zinnia_entry')

        # Removing M2M table for field sites on 'Entry'
        db.delete_table(db.shorten_name(u'zinnia_entry_sites'))

        # Removing M2M table for field related on 'Entry'
        db.delete_table(db.shorten_name(u'zinnia_entry_related'))

        # Removing M2M table for field authors on 'Entry'
        db.delete_table(db.shorten_name(u'zinnia_entry_authors'))

        # Removing M2M table for field categories on 'Entry'
        db.delete_table(db.shorten_name(u'zinnia_entry_categories'))

        # Deleting model 'Category'
        db.delete_table(u'zinnia_category')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'sites.site': {
            'Meta': {'ordering': "(u'domain',)", 'object_name': 'Site', 'db_table': "u'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'zinnia.category': {
            'Meta': {'ordering': "['title']", 'object_name': 'Category'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['zinnia.Category']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'zinnia.entry': {
            'Meta': {'ordering': "['-creation_date']", 'object_name': 'Entry', 'index_together': "[['slug', 'creation_date'], ['status', 'creation_date', 'start_publication', 'end_publication']]"},
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'entries'", 'blank': 'True', 'to': u"orm['auth.User']"}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'entries'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['zinnia.Category']"}),
            'comment_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'comment_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'content_template': ('django.db.models.fields.CharField', [], {'default': "'zinnia/_entry_detail.html'", 'max_length': '250'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'db_index': 'True'}),
            'detail_template': ('django.db.models.fields.CharField', [], {'default': "'entry_detail.html'", 'max_length': '250'}),
            'end_publication': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'excerpt': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'login_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'pingback_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pingback_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'related': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'related_rel_+'", 'null': 'True', 'to': "orm['zinnia.Entry']"}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'entries'", 'symmetrical': 'False', 'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'start_publication': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'trackback_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'trackback_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        }
    }

    complete_apps = ['zinnia']
