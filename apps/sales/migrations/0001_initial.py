import uuid
from decimal import Decimal
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [('core','0001_initial'), ('customers','0001_initial'), ('catalog','0001_initial'), migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(name='SalesOrder', fields=[('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),('created_at', models.DateTimeField(auto_now_add=True)),('updated_at', models.DateTimeField(auto_now=True)),('number', models.CharField(blank=True, db_index=True, max_length=40)),('status', models.CharField(choices=[('draft','Rascunho'),('confirmed','Confirmado'),('cancelled','Cancelado'),('completed','Concluído')], default='draft', max_length=20)),('total_amount', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=14)),('notes', models.TextField(blank=True)),('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sales_orders', to='customers.customer')),('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.organization'))], options={'ordering':['-created_at']}),
        migrations.CreateModel(name='SalesOrderItem', fields=[('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),('created_at', models.DateTimeField(auto_now_add=True)),('updated_at', models.DateTimeField(auto_now=True)),('description', models.CharField(blank=True, max_length=220)),('quantity', models.DecimalField(decimal_places=3, max_digits=12)),('unit_price', models.DecimalField(decimal_places=2, max_digits=12)),('subtotal', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=14)),('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='sales.salesorder')),('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sales_order_items', to='catalog.product'))], options={'ordering':['created_at']}),
    ]
