from datetime import date

from django.test import TestCase

from apps.academics.models import ClassGroup, GradeLevel, Subject, TeacherAssignment, TeacherProfile
from apps.saas.models import Tenant
from apps.schools.models import AcademicYear, School, SchoolUnit


class AcademicsTests(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(name='Tenant Acadêmico', slug='tenant-academico')
        self.school = School.objects.create(tenant=self.tenant, name='Colégio Acadêmico')
        self.unit = SchoolUnit.objects.create(tenant=self.tenant, school=self.school, name='Unidade Centro')
        self.academic_year = AcademicYear.objects.create(
            tenant=self.tenant,
            school=self.school,
            name='2026',
            year=2026,
            starts_at=date(2026, 2, 1),
            ends_at=date(2026, 12, 15),
        )

    def test_creates_minimal_academic_structure(self):
        grade_level = GradeLevel.objects.create(
            tenant=self.tenant,
            school=self.school,
            name='1º Ano',
            order=1,
            stage=GradeLevel.Stage.ELEMENTARY_1,
        )
        subject = Subject.objects.create(tenant=self.tenant, school=self.school, name='Matemática', code='MAT')
        class_group = ClassGroup.objects.create(
            tenant=self.tenant,
            school=self.school,
            unit=self.unit,
            academic_year=self.academic_year,
            grade_level=grade_level,
            name='1A',
            shift=ClassGroup.Shift.MORNING,
            max_students=30,
        )

        self.assertEqual(grade_level.slug, '1o-ano')
        self.assertEqual(subject.slug, 'matematica')
        self.assertEqual(class_group.slug, '1a')

    def test_creates_teacher_and_assignment(self):
        grade_level = GradeLevel.objects.create(tenant=self.tenant, school=self.school, name='2º Ano', order=2)
        subject = Subject.objects.create(tenant=self.tenant, school=self.school, name='Português')
        class_group = ClassGroup.objects.create(
            tenant=self.tenant,
            school=self.school,
            academic_year=self.academic_year,
            grade_level=grade_level,
            name='2A',
        )
        teacher = TeacherProfile.objects.create(
            tenant=self.tenant,
            school=self.school,
            full_name='Ana Professora',
            email='ana@example.com',
        )
        assignment = TeacherAssignment.objects.create(
            tenant=self.tenant,
            teacher=teacher,
            class_group=class_group,
            subject=subject,
            academic_year=self.academic_year,
        )

        self.assertEqual(assignment.teacher, teacher)
        self.assertEqual(assignment.subject, subject)
