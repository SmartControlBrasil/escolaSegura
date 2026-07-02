from django.test import TestCase

from apps.guardians.models import Guardian, GuardianStudentLink
from apps.saas.models import Tenant
from apps.schools.models import School
from apps.students.models import Student


class GuardianTests(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(name='Tenant Responsáveis', slug='tenant-responsaveis')
        self.school = School.objects.create(tenant=self.tenant, name='Colégio Família')
        self.student = Student.objects.create(
            tenant=self.tenant,
            school=self.school,
            full_name='Aluno Família',
        )

    def test_creates_guardian_and_student_link_with_permissions(self):
        guardian = Guardian.objects.create(
            tenant=self.tenant,
            school=self.school,
            full_name='Responsável Família',
            email='responsavel@example.com',
        )
        link = GuardianStudentLink.objects.create(
            tenant=self.tenant,
            guardian=guardian,
            student=self.student,
            relationship=GuardianStudentLink.Relationship.MOTHER,
            can_pickup=True,
            can_view_financial=True,
            is_primary=True,
        )

        self.assertTrue(link.can_pickup)
        self.assertTrue(link.can_view_financial)
        self.assertTrue(link.can_receive_messages)
        self.assertTrue(link.is_primary)
