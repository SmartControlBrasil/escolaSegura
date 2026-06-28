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
        ('catalog', '0001_initial'),
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Estimate',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('number', models.CharField(blank=True, db_index=True, max_length=40)),
                ('title', models.CharField(max_length=180)),
                ('status', models.CharField(choices=[('draft', 'Rascunho'), ('inspection', 'Em vistoria'), ('pricing', 'Em orçamento'), ('sent', 'Enviado'), ('approved', 'Aprovado'), ('rejected', 'Rejeitado'), ('cancelled', 'Cancelado')], default='draft', max_length=30)),
                ('service_location', models.CharField(blank=True, max_length=240)),
                ('visit_scheduled_at', models.DateTimeField(blank=True, null=True)),
                ('scope_summary', models.TextField(blank=True)),
                ('internal_notes', models.TextField(blank=True)),
                ('customer_message', models.TextField(blank=True)),
                ('terms_and_conditions', models.TextField(blank=True)),
                ('validity_days', models.PositiveIntegerField(default=7)),
                ('labor_amount', models.DecimalField(decimal_places=2, default='0.00', max_digits=14)),
                ('discount_amount', models.DecimalField(decimal_places=2, default='0.00', max_digits=14)),
                ('tax_amount', models.DecimalField(decimal_places=2, default='0.00', max_digits=14)),
                ('subtotal_amount', models.DecimalField(decimal_places=2, default='0.00', max_digits=14)),
                ('total_amount', models.DecimalField(decimal_places=2, default='0.00', max_digits=14)),
                ('assigned_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_estimates', to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_estimates', to=settings.AUTH_USER_MODEL)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='estimates', to='customers.customer')),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.organization')),
                ('sales_order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='estimates', to='sales.salesorder')),
            ],
            options={'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='EstimateLine',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('kind', models.CharField(choices=[('product', 'Produto'), ('service', 'Serviço'), ('material', 'Material'), ('labor', 'Mão de obra'), ('other', 'Outro')], default='service', max_length=30)),
                ('description', models.CharField(max_length=240)),
                ('unit', models.CharField(default='un', max_length=20)),
                ('quantity', models.DecimalField(decimal_places=3, default='1.000', max_digits=12)),
                ('unit_price', models.DecimalField(decimal_places=2, default='0.00', max_digits=12)),
                ('discount_amount', models.DecimalField(decimal_places=2, default='0.00', max_digits=12)),
                ('subtotal', models.DecimalField(decimal_places=2, default='0.00', max_digits=14)),
                ('sort_order', models.PositiveIntegerField(default=0)),
                ('notes', models.TextField(blank=True)),
                ('estimate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lines', to='estimates.estimate')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='estimate_lines', to='catalog.product')),
            ],
            options={'ordering': ['sort_order', 'created_at']},
        ),
        migrations.CreateModel(
            name='EstimateMeasurement',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('label', models.CharField(max_length=160)),
                ('value', models.DecimalField(decimal_places=3, max_digits=12)),
                ('unit', models.CharField(default='m', max_length=20)),
                ('notes', models.TextField(blank=True)),
                ('sort_order', models.PositiveIntegerField(default=0)),
                ('estimate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='measurements', to='estimates.estimate')),
            ],
            options={'ordering': ['sort_order', 'created_at']},
        ),
        migrations.CreateModel(
            name='EstimatePhoto',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(upload_to='estimates/photos/%Y/%m/')),
                ('category', models.CharField(choices=[('before', 'Antes do serviço'), ('measurement', 'Medição'), ('environment', 'Ambiente'), ('detail', 'Detalhe técnico'), ('document', 'Documento'), ('other', 'Outro')], default='before', max_length=30)),
                ('caption', models.CharField(blank=True, max_length=220)),
                ('measurement_notes', models.TextField(blank=True)),
                ('taken_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('estimate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='estimates.estimate')),
                ('uploaded_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['-taken_at']},
        ),
        migrations.CreateModel(
            name='EstimateContactMessage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('channel', models.CharField(choices=[('whatsapp', 'WhatsApp'), ('email', 'E-mail'), ('phone', 'Telefone'), ('internal', 'Interno')], default='whatsapp', max_length=30)),
                ('subject', models.CharField(blank=True, max_length=180)),
                ('body', models.TextField()),
                ('status', models.CharField(choices=[('draft', 'Rascunho'), ('approved', 'Aprovado'), ('sent', 'Enviado'), ('cancelled', 'Cancelado')], default='draft', max_length=30)),
                ('approved_by_human', models.BooleanField(default=False)),
                ('sent_at', models.DateTimeField(blank=True, null=True)),
                ('estimate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contact_messages', to='estimates.estimate')),
            ],
            options={'ordering': ['-created_at']},
        ),
    ]
