from datetime import date

from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.academics.models import ClassGroup, GradeLevel
from apps.saas.models import Tenant
from apps.schools.models import AcademicYear, School
from apps.students.models import Student, StudentEnrollment


class StudentTests(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(name='Tenant Alunos', slug='tenant-alunos')
        self.school = School.objects.create(tenant=self.tenant, name='Colégio Alunos')
        self.academic_year = AcademicYear.objects.create(
            tenant=self.tenant,
            school=self.school,
            name='2026',
            year=2026,
            starts_at=date(2026, 2, 1),
            ends_at=date(2026, 12, 15),
        )
        self.grade_level = GradeLevel.objects.create(tenant=self.tenant, school=self.school, name='3º Ano', order=3)
        self.class_group = ClassGroup.objects.create(
            tenant=self.tenant,
            school=self.school,
            academic_year=self.academic_year,
            grade_level=self.grade_level,
            name='3A',
        )

    def test_creates_student_linked_to_tenant_and_school(self):
        student = Student.objects.create(
            tenant=self.tenant,
            school=self.school,
            full_name='João Estudante',
            student_code='ALU-001',
        )

        self.assertEqual(student.tenant, self.tenant)
        self.assertEqual(student.school, self.school)

    def test_creates_active_enrollment(self):
        student = Student.objects.create(tenant=self.tenant, school=self.school, full_name='Maria Estudante')
        enrollment = StudentEnrollment.objects.create(
            tenant=self.tenant,
            student=student,
            school=self.school,
            academic_year=self.academic_year,
            class_group=self.class_group,
            status=StudentEnrollment.Status.ACTIVE,
        )

        self.assertEqual(enrollment.status, StudentEnrollment.Status.ACTIVE)

    def test_prevents_two_active_enrollments_for_same_student_and_year(self):
        student = Student.objects.create(tenant=self.tenant, school=self.school, full_name='Pedro Estudante')
        StudentEnrollment.objects.create(
            tenant=self.tenant,
            student=student,
            school=self.school,
            academic_year=self.academic_year,
            class_group=self.class_group,
            status=StudentEnrollment.Status.ACTIVE,
        )
        duplicated = StudentEnrollment(
            tenant=self.tenant,
            student=student,
            school=self.school,
            academic_year=self.academic_year,
            class_group=self.class_group,
            status=StudentEnrollment.Status.ACTIVE,
        )

        with self.assertRaises(ValidationError):
            duplicated.full_clean()
