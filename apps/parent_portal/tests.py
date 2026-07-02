from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.academics.models import ClassGroup, GradeLevel, Subject, TeacherProfile
from apps.assessments.models import ReportCard, ReportCardEntry, SchoolTerm
from apps.attendance.models import AttendanceRecord, AttendanceSession
from apps.communication.models import Announcement, AnnouncementAudience, AuthorizationRequest, Message, MessageThread
from apps.guardians.models import Guardian, GuardianStudentLink
from apps.saas.models import Tenant
from apps.schools.models import AcademicYear, School
from apps.students.models import Student, StudentEnrollment

User = get_user_model()


class ParentPortalTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='familia',
            email='responsavel@example.com',
            password='testpassword',
        )
        self.other_user = User.objects.create_user(
            username='semguardian',
            email='semguardian@example.com',
            password='testpassword',
        )
        self.tenant = Tenant.objects.create(name='Tenant Família', slug='tenant-familia')
        self.school = School.objects.create(tenant=self.tenant, name='Colégio Família')
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
            name='7º Ano',
            order=7,
            stage=GradeLevel.Stage.ELEMENTARY_2,
        )
        self.subject = Subject.objects.create(tenant=self.tenant, school=self.school, name='Matemática')
        self.class_group = ClassGroup.objects.create(
            tenant=self.tenant,
            school=self.school,
            academic_year=self.academic_year,
            grade_level=self.grade_level,
            name='7A',
        )
        self.student = Student.objects.create(
            tenant=self.tenant,
            school=self.school,
            full_name='Aluno Família',
            student_code='FAM-001',
        )
        self.other_student = Student.objects.create(
            tenant=self.tenant,
            school=self.school,
            full_name='Aluno Não Vinculado',
            student_code='FAM-002',
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
            full_name='Professor Família',
        )
        self.guardian = Guardian.objects.create(
            tenant=self.tenant,
            school=self.school,
            full_name='Responsável Família',
            email='responsavel@example.com',
        )
        self.link = GuardianStudentLink.objects.create(
            tenant=self.tenant,
            guardian=self.guardian,
            student=self.student,
            relationship=GuardianStudentLink.Relationship.LEGAL_GUARDIAN,
            can_authorize_events=True,
            is_active=True,
        )
        self.session = AttendanceSession.objects.create(
            tenant=self.tenant,
            school=self.school,
            academic_year=self.academic_year,
            class_group=self.class_group,
            subject=self.subject,
            teacher=self.teacher,
            session_date=date(2026, 3, 10),
        )
        self.record = AttendanceRecord.objects.create(
            tenant=self.tenant,
            session=self.session,
            student=self.student,
            enrollment=self.enrollment,
            status=AttendanceRecord.Status.PRESENT,
        )
        self.announcement = Announcement.objects.create(
            tenant=self.tenant,
            school=self.school,
            academic_year=self.academic_year,
            title='Comunicado Família',
            body='Reunião escolar.',
        )
        self.announcement.publish()
        AnnouncementAudience.objects.create(
            tenant=self.tenant,
            announcement=self.announcement,
            audience_type=AnnouncementAudience.AudienceType.ALL_SCHOOL,
        )
        self.thread = MessageThread.objects.create(
            tenant=self.tenant,
            school=self.school,
            student=self.student,
            guardian=self.guardian,
            subject='Conversa com a escola',
        )
        Message.objects.create(
            tenant=self.tenant,
            thread=self.thread,
            sender_guardian=self.guardian,
            body='Olá, escola.',
        )
        self.authorization = AuthorizationRequest.objects.create(
            tenant=self.tenant,
            school=self.school,
            student=self.student,
            title='Autorização de passeio',
            description='Passeio pedagógico.',
            request_type=AuthorizationRequest.RequestType.FIELD_TRIP,
        )
        self.term = SchoolTerm.objects.create(
            tenant=self.tenant,
            school=self.school,
            academic_year=self.academic_year,
            name='1º Bimestre',
            order=1,
            is_current=True,
        )
        self.report_card = ReportCard.objects.create(
            tenant=self.tenant,
            school=self.school,
            academic_year=self.academic_year,
            term=self.term,
            student=self.student,
            enrollment=self.enrollment,
            status=ReportCard.Status.PUBLISHED,
        )
        ReportCardEntry.objects.create(
            tenant=self.tenant,
            report_card=self.report_card,
            subject=self.subject,
            average_score=Decimal('8.50'),
            absences_count=1,
            teacher_comments='Bom desempenho.',
        )

    def test_anonymous_user_is_redirected_from_dashboard(self):
        response = self.client.get('/familia/')
        self.assertRedirects(response, '/app/login/?next=/familia/')

    def test_logged_user_without_guardian_email_sees_empty_dashboard(self):
        self.client.login(username='semguardian', password='testpassword')
        response = self.client.get('/familia/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nenhum aluno vinculado')

    def test_logged_user_with_guardian_email_sees_linked_student(self):
        self.client.login(username='familia', password='testpassword')
        response = self.client.get('/familia/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Aluno Família')

    def test_linked_student_detail_loads(self):
        self.client.login(username='familia', password='testpassword')
        response = self.client.get(f'/familia/alunos/{self.student.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Resumo')
        self.assertContains(response, 'Aluno Família')

    def test_unlinked_student_detail_returns_404(self):
        self.client.login(username='familia', password='testpassword')
        response = self.client.get(f'/familia/alunos/{self.other_student.id}/')
        self.assertEqual(response.status_code, 404)

    def test_linked_student_attendance_loads(self):
        self.client.login(username='familia', password='testpassword')
        response = self.client.get(f'/familia/alunos/{self.student.id}/frequencia/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Frequência')
        self.assertContains(response, 'Presente')

    def test_linked_student_announcements_loads(self):
        self.client.login(username='familia', password='testpassword')
        response = self.client.get(f'/familia/alunos/{self.student.id}/comunicados/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Comunicado Família')

    def test_linked_student_messages_loads(self):
        self.client.login(username='familia', password='testpassword')
        response = self.client.get(f'/familia/alunos/{self.student.id}/mensagens/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Conversa com a escola')

    def test_linked_student_authorizations_loads(self):
        self.client.login(username='familia', password='testpassword')
        response = self.client.get(f'/familia/alunos/{self.student.id}/autorizacoes/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Autorização de passeio')

    def test_linked_student_report_card_loads(self):
        self.client.login(username='familia', password='testpassword')
        response = self.client.get(f'/familia/alunos/{self.student.id}/boletim/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Boletim')
        self.assertContains(response, '8,50')
