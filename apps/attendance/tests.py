from datetime import date

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from apps.academics.models import ClassGroup, GradeLevel, Subject, TeacherProfile
from apps.attendance.models import AbsenceJustification, AttendanceRecord, AttendanceSession
from apps.saas.models import Tenant
from apps.schools.models import AcademicYear, School
from apps.students.models import Student, StudentEnrollment


class AttendanceTests(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(name='Tenant Frequência', slug='tenant-frequencia')
        self.school = School.objects.create(tenant=self.tenant, name='Colégio Frequência')
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
            name='4º Ano',
            order=4,
            stage=GradeLevel.Stage.ELEMENTARY_1,
        )
        self.subject = Subject.objects.create(tenant=self.tenant, school=self.school, name='Matemática')
        self.class_group = ClassGroup.objects.create(
            tenant=self.tenant,
            school=self.school,
            academic_year=self.academic_year,
            grade_level=self.grade_level,
            name='4A',
        )
        self.student = Student.objects.create(
            tenant=self.tenant,
            school=self.school,
            full_name='Aluno Frequência',
            student_code='FREQ-001',
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
            full_name='Professora Frequência',
        )

    def create_session(self, status=AttendanceSession.Status.OPEN):
        return AttendanceSession.objects.create(
            tenant=self.tenant,
            school=self.school,
            academic_year=self.academic_year,
            class_group=self.class_group,
            subject=self.subject,
            teacher=self.teacher,
            session_date=date(2026, 3, 10),
            session_number=1,
            status=status,
        )

    def test_create_attendance_session(self):
        session = self.create_session()

        self.assertEqual(session.status, AttendanceSession.Status.OPEN)
        self.assertTrue(session.is_editable)

    def test_closed_session_is_not_editable(self):
        session = self.create_session(status=AttendanceSession.Status.CLOSED)

        self.assertFalse(session.is_editable)

    def test_create_attendance_record(self):
        session = self.create_session()
        record = AttendanceRecord.objects.create(
            tenant=self.tenant,
            session=session,
            student=self.student,
            enrollment=self.enrollment,
            status=AttendanceRecord.Status.PRESENT,
        )

        self.assertEqual(record.status, AttendanceRecord.Status.PRESENT)
        self.assertFalse(record.is_absence)

    def test_absent_record_requires_justification(self):
        session = self.create_session()
        record = AttendanceRecord.objects.create(
            tenant=self.tenant,
            session=session,
            student=self.student,
            enrollment=self.enrollment,
            status=AttendanceRecord.Status.ABSENT,
        )

        self.assertTrue(record.is_absence)
        self.assertTrue(record.requires_justification)

    def test_prevent_duplicate_record_for_same_student_and_session(self):
        session = self.create_session()
        AttendanceRecord.objects.create(
            tenant=self.tenant,
            session=session,
            student=self.student,
            enrollment=self.enrollment,
        )

        with self.assertRaises((IntegrityError, ValidationError)):
            AttendanceRecord.objects.create(
                tenant=self.tenant,
                session=session,
                student=self.student,
                enrollment=self.enrollment,
            )

    def test_attendance_record_validates_student_tenant(self):
        session = self.create_session()
        other_tenant = Tenant.objects.create(name='Outro Tenant', slug='outro-tenant')
        other_school = School.objects.create(tenant=other_tenant, name='Outra Escola')
        other_student = Student.objects.create(
            tenant=other_tenant,
            school=other_school,
            full_name='Aluno de Outro Tenant',
        )
        record = AttendanceRecord(
            tenant=self.tenant,
            session=session,
            student=other_student,
            status=AttendanceRecord.Status.PRESENT,
        )

        with self.assertRaises(ValidationError):
            record.full_clean()

    def test_approve_absence_justification_marks_record_as_justified(self):
        session = self.create_session()
        record = AttendanceRecord.objects.create(
            tenant=self.tenant,
            session=session,
            student=self.student,
            enrollment=self.enrollment,
            status=AttendanceRecord.Status.ABSENT,
        )
        justification = AbsenceJustification.objects.create(
            tenant=self.tenant,
            record=record,
            reason='Atestado médico.',
        )

        justification.approve(notes='Documento aceito.')
        record.refresh_from_db()

        self.assertEqual(justification.status, AbsenceJustification.Status.APPROVED)
        self.assertEqual(record.status, AttendanceRecord.Status.JUSTIFIED)

    def test_reject_absence_justification_does_not_change_record_status(self):
        session = self.create_session()
        record = AttendanceRecord.objects.create(
            tenant=self.tenant,
            session=session,
            student=self.student,
            enrollment=self.enrollment,
            status=AttendanceRecord.Status.ABSENT,
        )
        justification = AbsenceJustification.objects.create(
            tenant=self.tenant,
            record=record,
            reason='Justificativa insuficiente.',
        )

        justification.reject(notes='Sem documento comprobatório.')
        record.refresh_from_db()

        self.assertEqual(justification.status, AbsenceJustification.Status.REJECTED)
        self.assertEqual(record.status, AttendanceRecord.Status.ABSENT)
