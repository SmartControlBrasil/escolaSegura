import uuid
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(name='IntegrationProvider', fields=[('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),('created_at', models.DateTimeField(auto_now_add=True)),('updated_at', models.DateTimeField(auto_now=True)),('name', models.CharField(max_length=120)),('slug', models.SlugField(max_length=120, unique=True)),('base_url', models.URLField(blank=True)),('is_active', models.BooleanField(default=True)),('config', models.JSONField(blank=True, default=dict))]),
        migrations.CreateModel(name='WebhookEvent', fields=[('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),('created_at', models.DateTimeField(auto_now_add=True)),('updated_at', models.DateTimeField(auto_now=True)),('event_type', models.CharField(max_length=120)),('payload', models.JSONField(blank=True, default=dict)),('status', models.CharField(default='received', max_length=30)),('processed_at', models.DateTimeField(blank=True, null=True)),('error_message', models.TextField(blank=True)),('provider', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='integrations.integrationprovider'))]),
    ]
