from datetime import date
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.academics.models import ClassGroup, GradeLevel, Subject, TeacherProfile
from apps.assessments.models import Assessment, AssessmentGrade, ReportCard, ReportCardEntry, SchoolTerm
from apps.saas.models import Tenant
from apps.schools.models import AcademicYear, School
from apps.students.models import Student, StudentEnrollment


class AssessmentTests(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(name='Tenant Avaliações', slug='tenant-avaliacoes')
        self.school = School.objects.create(tenant=self.tenant, name='Colégio Avaliações')
        self.academic_year = AcademicYear.objects.create(
            tenant=self.tenant,
            school=self.school,
            name='2026',
            year=2026,
            starts_at=date(2026, 2, 1),
            ends_at=date(2026, 12, 15),
        )
        self.grade_level = GradeLevel.objects.create(
            tenant=self.tenant,
            school=self.school,
            name='6º Ano',
            order=6,
            stage=GradeLevel.Stage.ELEMENTARY_2,
        )
        self.subject = Subject.objects.create(tenant=self.tenant, school=self.school, name='Matemática')
        self.class_group = ClassGroup.objects.create(
            tenant=self.tenant,
            school=self.school,
            academic_year=self.academic_year,
            grade_level=self.grade_level,
            name='6A',
        )
        self.student = Student.objects.create(
            tenant=self.tenant,
            school=self.school,
            full_name='Aluno Avaliação',
            student_code='AVA-001',
        )
        self.enrollment = StudentEnrollment.objects.create(
            tenant=self.tenant,
            student=self.student,
            school=self.school,
            academic_year=self.academic_year,
            class_group=self.class_group,
            status=StudentEnrollment.Status.ACTIVE,
        )
        self.teacher = TeacherProfile.objects.create(
            tenant=self.tenant,
            school=self.school,
            full_name='Professor Avaliação',
        )

    def create_term(self):
        return SchoolTerm.objects.create(
            tenant=self.tenant,
            school=self.school,
            academic_year=self.academic_year,
            name='1º Bimestre',
            order=1,
            starts_at=date(2026, 2, 1),
            ends_at=date(2026, 4, 30),
            is_current=True,
        )

    def create_assessment(self, max_score=Decimal('10.00'), weight=Decimal('1.00')):
        return Assessment.objects.create(
            tenant=self.tenant,
            school=self.school,
            academic_year=self.academic_year,
            term=self.create_term(),
            class_group=self.class_group,
            subject=self.subject,
            teacher=self.teacher,
            title='Prova 1',
            assessment_type=Assessment.AssessmentType.TEST,
            assessment_date=date(2026, 3, 15),
            max_score=max_score,
            weight=weight,
        )

    def test_create_school_term(self):
        term = self.create_term()

        self.assertEqual(term.slug, '1o-bimestre')
        self.assertTrue(term.is_current)

    def test_school_term_rejects_invalid_dates(self):
        term = SchoolTerm(
            tenant=self.tenant,
            school=self.school,
            academic_year=self.academic_year,
            name='Etapa inválida',
            starts_at=date(2026, 5, 1),
            ends_at=date(2026, 4, 30),
        )

        with self.assertRaises(ValidationError):
            term.full_clean()

    def test_create_assessment(self):
        assessment = self.create_assessment()

        self.assertEqual(assessment.max_score, Decimal('10.00'))
        self.assertEqual(assessment.weight, Decimal('1.00'))
        self.assertFalse(assessment.is_published)

    def test_assessment_publish_sets_published_at(self):
        assessment = self.create_assessment()

        assessment.publish()

        self.assertTrue(assessment.is_published)
        self.assertIsNotNone(assessment.published_at)

    def test_assessment_grade_percentage(self):
        assessment = self.create_assessment(max_score=Decimal('10.00'))
        grade = AssessmentGrade.objects.create(
            tenant=self.tenant,
            assessment=assessment,
            student=self.student,
            enrollment=self.enrollment,
            score=Decimal('8.00'),
        )

        self.assertEqual(grade.percentage, Decimal('80.0'))

    def test_assessment_grade_rejects_score_above_max(self):
        assessment = self.create_assessment(max_score=Decimal('10.00'))
        grade = AssessmentGrade(
            tenant=self.tenant,
            assessment=assessment,
            student=self.student,
            enrollment=self.enrollment,
            score=Decimal('11.00'),
        )

        with self.assertRaises(ValidationError):
            grade.full_clean()

    def test_assessment_grade_validates_student_tenant(self):
        assessment = self.create_assessment()
        other_tenant = Tenant.objects.create(name='Outro Tenant', slug='outro-tenant-avaliacao')
        other_school = School.objects.create(tenant=other_tenant, name='Outra Escola')
        other_student = Student.objects.create(
            tenant=other_tenant,
            school=other_school,
            full_name='Aluno de outro tenant',
        )
        grade = AssessmentGrade(
            tenant=self.tenant,
            assessment=assessment,
            student=other_student,
            score=Decimal('7.00'),
        )

        with self.assertRaises(ValidationError):
            grade.full_clean()

    def test_create_report_card(self):
        term = self.create_term()
        report_card = ReportCard.objects.create(
            tenant=self.tenant,
            school=self.school,
            academic_year=self.academic_year,
            term=term,
            student=self.student,
            enrollment=self.enrollment,
        )

        self.assertEqual(report_card.status, ReportCard.Status.DRAFT)
        self.assertFalse(report_card.is_published)

    def test_report_card_publish(self):
        term = self.create_term()
        report_card = ReportCard.objects.create(
            tenant=self.tenant,
            school=self.school,
            academic_year=self.academic_year,
            term=term,
            student=self.student,
            enrollment=self.enrollment,
        )

        report_card.publish()

        self.assertEqual(report_card.status, ReportCard.Status.PUBLISHED)
        self.assertIsNotNone(report_card.published_at)

    def test_report_card_entry_below_average(self):
        term = self.create_term()
        report_card = ReportCard.objects.create(
            tenant=self.tenant,
            school=self.school,
            academic_year=self.academic_year,
            term=term,
            student=self.student,
            enrollment=self.enrollment,
        )
        entry = ReportCardEntry.objects.create(
            tenant=self.tenant,
            report_card=report_card,
            subject=self.subject,
            average_score=Decimal('5.50'),
        )

        self.assertTrue(entry.is_below_average)

    def test_report_card_entry_rejects_average_above_10(self):
        term = self.create_term()
        report_card = ReportCard.objects.create(
            tenant=self.tenant,
            school=self.school,
            academic_year=self.academic_year,
            term=term,
            student=self.student,
            enrollment=self.enrollment,
        )
        entry = ReportCardEntry(
            tenant=self.tenant,
            report_card=report_card,
            subject=self.subject,
            average_score=Decimal('10.50'),
        )

        with self.assertRaises(ValidationError):
            entry.full_clean()
