import uuid
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(name='Organization', fields=[('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),('created_at', models.DateTimeField(auto_now_add=True)),('updated_at', models.DateTimeField(auto_now=True)),('name', models.CharField(max_length=180)),('legal_name', models.CharField(blank=True, max_length=220)),('document', models.CharField(blank=True, db_index=True, max_length=32)),('email', models.EmailField(blank=True, max_length=254)),('phone', models.CharField(blank=True, max_length=32)),('status', models.CharField(choices=[('active', 'Ativa'), ('inactive', 'Inativa')], default='active', max_length=20))], options={'ordering':['name']}),
        migrations.CreateModel(name='SystemSetting', fields=[('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),('created_at', models.DateTimeField(auto_now_add=True)),('updated_at', models.DateTimeField(auto_now=True)),('key', models.SlugField(max_length=120, unique=True)),('value', models.JSONField(blank=True, default=dict)),('description', models.TextField(blank=True)),('is_sensitive', models.BooleanField(default=False))], options={'ordering':['key']}),
        migrations.CreateModel(name='Branch', fields=[('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),('created_at', models.DateTimeField(auto_now_add=True)),('updated_at', models.DateTimeField(auto_now=True)),('name', models.CharField(max_length=160)),('city', models.CharField(blank=True, max_length=120)),('state', models.CharField(blank=True, max_length=2)),('is_headquarters', models.BooleanField(default=False)),('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='branches', to='core.organization'))], options={'ordering':['organization__name','name'], 'unique_together': {('organization','name')}}),
    ]
