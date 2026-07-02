from django.core.management import call_command
from django.test import TestCase

from apps.saas.models import SubscriptionPlan, Tenant, TenantSubscription, TenantUsage


class SaasFoundationTests(TestCase):
    def test_seed_creates_four_plans(self):
        call_command('seed_escola_segura_plans')

        self.assertEqual(SubscriptionPlan.objects.count(), 4)
        self.assertTrue(SubscriptionPlan.objects.filter(slug='essencial').exists())
        self.assertTrue(SubscriptionPlan.objects.filter(slug='academico').exists())
        self.assertTrue(SubscriptionPlan.objects.filter(slug='gestao').exists())
        self.assertTrue(SubscriptionPlan.objects.filter(slug='ia').exists())

    def test_feature_gate_works(self):
        call_command('seed_escola_segura_plans')

        essencial = SubscriptionPlan.objects.get(slug='essencial')
        ia = SubscriptionPlan.objects.get(slug='ia')

        self.assertTrue(essencial.includes_feature('students'))
        self.assertFalse(essencial.includes_feature('ai_assistant'))
        self.assertTrue(ia.includes_feature('ai_assistant'))

    def test_active_subscription_can_use_feature(self):
        call_command('seed_escola_segura_plans')
        tenant = Tenant.objects.create(name='Escola Modelo', slug='escola-modelo', status=Tenant.Status.ACTIVE)
        plan = SubscriptionPlan.objects.get(slug='academico')
        subscription = TenantSubscription.objects.create(
            tenant=tenant,
            plan=plan,
            status=TenantSubscription.Status.ACTIVE,
        )

        self.assertTrue(subscription.can_use_feature('documents'))

    def test_suspended_subscription_cannot_use_feature(self):
        call_command('seed_escola_segura_plans')
        tenant = Tenant.objects.create(name='Escola Pausada', slug='escola-pausada', status=Tenant.Status.ACTIVE)
        plan = SubscriptionPlan.objects.get(slug='gestao')
        subscription = TenantSubscription.objects.create(
            tenant=tenant,
            plan=plan,
            status=TenantSubscription.Status.SUSPENDED,
        )

        self.assertFalse(subscription.can_use_feature('whatsapp'))

    def test_tenant_usage_detects_students_limit(self):
        call_command('seed_escola_segura_plans')
        tenant = Tenant.objects.create(name='Escola Limite', slug='escola-limite', status=Tenant.Status.ACTIVE)
        plan = SubscriptionPlan.objects.get(slug='essencial')
        TenantSubscription.objects.create(
            tenant=tenant,
            plan=plan,
            status=TenantSubscription.Status.ACTIVE,
        )
        usage = TenantUsage.objects.create(tenant=tenant, students_count=100)

        self.assertTrue(usage.is_students_limit_reached())
