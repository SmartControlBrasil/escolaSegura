from decimal import Decimal
from django.db import transaction
from apps.catalog.infrastructure.models import Product
from apps.estimates.infrastructure.models import Estimate, EstimateContactMessage, EstimateLine


class EstimateService:
    @staticmethod
    @transaction.atomic
    def create_estimate(*, customer=None, organization=None, created_by=None, title='Novo orçamento', lines=None, **extra):
        estimate = Estimate.objects.create(
            customer=customer,
            organization=organization or getattr(customer, 'organization', None),
            created_by=created_by,
            title=title,
            **extra,
        )
        estimate.ensure_number()
        for row in lines or []:
            product = None
            if row.get('product'):
                product = Product.objects.get(id=row['product'])
            EstimateLine.objects.create(
                estimate=estimate,
                product=product,
                kind=row.get('kind') or EstimateLine.Kind.SERVICE,
                description=row.get('description') or getattr(product, 'name', 'Item do orçamento'),
                unit=row.get('unit') or getattr(product, 'unit', 'un'),
                quantity=row.get('quantity') or Decimal('1.000'),
                unit_price=row.get('unit_price') or getattr(product, 'sale_price', Decimal('0.00')),
                discount_amount=row.get('discount_amount') or Decimal('0.00'),
                notes=row.get('notes', ''),
            )
        estimate.recalculate_totals()
        return estimate

    @staticmethod
    def generate_first_contact_message(estimate, channel='whatsapp'):
        customer_name = getattr(estimate.customer, 'name', '') or 'cliente'
        location = estimate.service_location or 'local informado'
        body = (
            f'Olá, {customer_name}! Aqui é da equipe técnica. '\
            f'Abrimos o orçamento {estimate.number or estimate.ensure_number()} para: {estimate.title}. '\
            f'Na vistoria vamos registrar fotos, medidas e observações do serviço em {location}. '\
            'Depois disso, montaremos uma proposta editável e enviaremos para sua aprovação. '
            'Se puder, confirme o melhor horário para a visita.'
        )
        return EstimateContactMessage.objects.create(
            estimate=estimate,
            channel=channel,
            subject=f'Primeiro contato - {estimate.number}',
            body=body,
        )
