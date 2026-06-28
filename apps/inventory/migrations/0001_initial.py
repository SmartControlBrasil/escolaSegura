import uuid
from decimal import Decimal
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [('core','0001_initial'), ('catalog','0001_initial'), migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(name='StockLocation', fields=[('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),('created_at', models.DateTimeField(auto_now_add=True)),('updated_at', models.DateTimeField(auto_now=True)),('name', models.CharField(max_length=160)),('code', models.CharField(blank=True, max_length=40)),('is_active', models.BooleanField(default=True)),('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.organization'))], options={'ordering':['name'], 'unique_together': {('organization','code')}}),
        migrations.CreateModel(name='StockBalance', fields=[('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),('created_at', models.DateTimeField(auto_now_add=True)),('updated_at', models.DateTimeField(auto_now=True)),('quantity', models.DecimalField(decimal_places=3, default=Decimal('0.000'), max_digits=14)),('minimum_quantity', models.DecimalField(decimal_places=3, default=Decimal('0.000'), max_digits=14)),('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='balances', to='inventory.stocklocation')),('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stock_balances', to='catalog.product'))], options={'unique_together': {('product','location')}}),
        migrations.CreateModel(name='StockMovement', fields=[('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),('created_at', models.DateTimeField(auto_now_add=True)),('updated_at', models.DateTimeField(auto_now=True)),('type', models.CharField(choices=[('in','Entrada'),('out','Saída'),('adjust','Ajuste')], max_length=20)),('quantity', models.DecimalField(decimal_places=3, max_digits=14)),('reason', models.CharField(blank=True, max_length=160)),('reference', models.CharField(blank=True, max_length=120)),('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),('location', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='movements', to='inventory.stocklocation')),('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='stock_movements', to='catalog.product'))], options={'ordering':['-created_at']}),
    ]
