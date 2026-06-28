from django.db import transaction
from apps.catalog.infrastructure.models import Product
from apps.sales.infrastructure.models import SalesOrder, SalesOrderItem

class SalesOrderService:
    @staticmethod
    @transaction.atomic
    def create_order(*, customer, organization=None, created_by=None, items=None, notes=''):
        order = SalesOrder.objects.create(customer=customer, organization=organization, created_by=created_by, notes=notes)
        for row in items or []:
            product = Product.objects.get(id=row['product'])
            SalesOrderItem.objects.create(
                order=order,
                product=product,
                description=row.get('description') or product.name,
                quantity=row['quantity'],
                unit_price=row.get('unit_price') or product.sale_price,
            )
        order.number = f'PED-{str(order.id)[:8].upper()}'
        order.save(update_fields=['number', 'updated_at'])
        order.recalculate_total()
        return order
