import uuid
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [('core','0001_initial')]
    operations = [
        migrations.CreateModel(name='HtmlPage', fields=[('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),('created_at', models.DateTimeField(auto_now_add=True)),('updated_at', models.DateTimeField(auto_now=True)),('title', models.CharField(max_length=180)),('slug', models.SlugField(max_length=180)),('template_name', models.CharField(default='pages/generic.html', max_length=180)),('html', models.TextField(blank=True)),('content', models.JSONField(blank=True, default=dict)),('seo_title', models.CharField(blank=True, max_length=180)),('seo_description', models.CharField(blank=True, max_length=260)),('status', models.CharField(choices=[('draft','Rascunho'),('published','Publicada'),('archived','Arquivada')], default='draft', max_length=20)),('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.organization'))], options={'ordering':['title'], 'unique_together': {('organization','slug')}}),
    ]
