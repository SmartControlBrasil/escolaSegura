import uuid
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [('core','0001_initial'), migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(name='ActivityLog', fields=[('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),('created_at', models.DateTimeField(auto_now_add=True)),('updated_at', models.DateTimeField(auto_now=True)),('action', models.CharField(db_index=True, max_length=120)),('object_type', models.CharField(blank=True, max_length=120)),('object_id', models.CharField(blank=True, max_length=80)),('ip_address', models.GenericIPAddressField(blank=True, null=True)),('user_agent', models.TextField(blank=True)),('metadata', models.JSONField(blank=True, default=dict)),('actor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.organization'))], options={'ordering':['-created_at']}),
        migrations.CreateModel(name='Attachment', fields=[('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),('created_at', models.DateTimeField(auto_now_add=True)),('updated_at', models.DateTimeField(auto_now=True)),('file', models.FileField(upload_to='attachments/%Y/%m/')),('title', models.CharField(blank=True, max_length=180)),('content_type', models.CharField(blank=True, max_length=120)),('object_type', models.CharField(blank=True, max_length=120)),('object_id', models.CharField(blank=True, max_length=80)),('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.organization')),('uploaded_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL))], options={'ordering':['-created_at']}),
    ]
