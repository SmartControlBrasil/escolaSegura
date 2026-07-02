from datetime import date

from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.saas.models import Tenant
from apps.schools.models import AcademicYear, School


class SchoolTests(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(name='EscolaSegura Demo', slug='escolasegura-demo')

    def test_creates_school_linked_to_tenant_and_generates_slug(self):
        school = School.objects.create(tenant=self.tenant, name='Colégio Modelo')

        self.assertEqual(school.tenant, self.tenant)
        self.assertEqual(school.slug, 'colegio-modelo')

    def test_academic_year_validates_end_date_after_start_date(self):
        school = School.objects.create(tenant=self.tenant, name='Colégio Modelo')
        academic_year = AcademicYear(
            tenant=self.tenant,
            school=school,
            name='2026',
            year=2026,
            starts_at=date(2026, 2, 1),
            ends_at=date(2026, 1, 31),
        )

        with self.assertRaises(ValidationError):
            academic_year.full_clean()
