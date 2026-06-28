from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(upload_to='catalog/products/%Y/%m/')),
                ('kind', models.CharField(choices=[('primary', 'Principal'), ('gallery', 'Galeria'), ('technical', 'Técnica'), ('before_after', 'Antes/depois'), ('document', 'Documento')], default='gallery', max_length=30)),
                ('title', models.CharField(blank=True, max_length=160)),
                ('caption', models.TextField(blank=True)),
                ('alt_text', models.CharField(blank=True, max_length=180)),
                ('sort_order', models.PositiveIntegerField(default=0)),
                ('is_public', models.BooleanField(default=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='catalog.product')),
            ],
            options={
                'ordering': ['product__name', 'sort_order', 'created_at'],
            },
        ),
    ]
