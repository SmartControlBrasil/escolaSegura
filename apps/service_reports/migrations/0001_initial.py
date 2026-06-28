from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
        ('customers', '0001_initial'),
        ('estimates', '0001_initial'),
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceReport',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('number', models.CharField(blank=True, db_index=True, max_length=40)),
                ('title', models.CharField(max_length=180)),
                ('status', models.CharField(choices=[('draft', 'Rascunho'), ('in_progress', 'Em execução'), ('completed', 'Concluído'), ('delivered', 'Entregue'), ('approved', 'Aprovado pelo cliente'), ('cancelled', 'Cancelado')], default='draft', max_length=30)),
                ('service_date', models.DateField(default=django.utils.timezone.localdate)),
                ('service_location', models.CharField(blank=True, max_length=240)),
                ('technician_name', models.CharField(blank=True, max_length=160)),
                ('problem_reported', models.TextField(blank=True)),
                ('service_performed', models.TextField(blank=True)),
                ('recommendations', models.TextField(blank=True)),
                ('customer_signature_name', models.CharField(blank=True, max_length=160)),
                ('started_at', models.DateTimeField(blank=True, null=True)),
                ('finished_at', models.DateTimeField(blank=True, null=True)),
                ('total_amount', models.DecimalField(decimal_places=2, default='0.00', max_digits=14)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='service_reports', to='customers.customer')),
                ('estimate', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='service_reports', to='estimates.estimate')),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.organization')),
                ('sales_order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='service_reports', to='sales.salesorder')),
            ],
            options={'ordering': ['-service_date', '-created_at']},
        ),
        migrations.CreateModel(
            name='ServiceReportItem',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('description', models.CharField(max_length=240)),
                ('quantity', models.DecimalField(decimal_places=3, default='1.000', max_digits=12)),
                ('unit', models.CharField(default='h', max_length=20)),
                ('unit_price', models.DecimalField(decimal_places=2, default='0.00', max_digits=12)),
                ('subtotal', models.DecimalField(decimal_places=2, default='0.00', max_digits=14)),
                ('is_billable', models.BooleanField(default=True)),
                ('notes', models.TextField(blank=True)),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='service_reports.servicereport')),
            ],
            options={'ordering': ['created_at']},
        ),
        migrations.CreateModel(
            name='ServiceReportPhoto',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(upload_to='service-reports/photos/%Y/%m/')),
                ('category', models.CharField(choices=[('before', 'Antes'), ('during', 'Durante'), ('after', 'Depois'), ('evidence', 'Evidência técnica'), ('document', 'Documento'), ('other', 'Outro')], default='evidence', max_length=30)),
                ('caption', models.CharField(blank=True, max_length=220)),
                ('technical_notes', models.TextField(blank=True)),
                ('taken_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='service_reports.servicereport')),
                ('uploaded_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['-taken_at']},
        ),
    ]
