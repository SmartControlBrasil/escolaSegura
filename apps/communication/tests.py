from datetime import date

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from apps.academics.models import ClassGroup, GradeLevel
from apps.communication.models import (
    Announcement,
    AnnouncementAudience,
    AnnouncementReadReceipt,
    AuthorizationRequest,
    AuthorizationResponse,
    Message,
    MessageThread,
)
from apps.guardians.models import Guardian, GuardianStudentLink
from apps.saas.models import Tenant
from apps.schools.models import AcademicYear, School
from apps.students.models import Student, StudentEnrollment


class CommunicationTests(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(name='Tenant Comunicação', slug='tenant-comunicacao')
        self.school = School.objects.create(tenant=self.tenant, name='Colégio Comunicação')
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
            name='5º Ano',
            order=5,
            stage=GradeLevel.Stage.ELEMENTARY_1,
        )
        self.class_group = ClassGroup.objects.create(
            tenant=self.tenant,
            school=self.school,
            academic_year=self.academic_year,
            grade_level=self.grade_level,
            name='5A',
        )
        self.student = Student.objects.create(
            tenant=self.tenant,
            school=self.school,
            full_name='Aluno Comunicação',
            student_code='COM-001',
        )
        self.enrollment = StudentEnrollment.objects.create(
            tenant=self.tenant,
            student=self.student,
            school=self.school,
            academic_year=self.academic_year,
            class_group=self.class_group,
            status=StudentEnrollment.Status.ACTIVE,
        )
        self.guardian = Guardian.objects.create(
            tenant=self.tenant,
            school=self.school,
            full_name='Responsável Comunicação',
        )
        self.link = GuardianStudentLink.objects.create(
            tenant=self.tenant,
            guardian=self.guardian,
            student=self.student,
            relationship=GuardianStudentLink.Relationship.LEGAL_GUARDIAN,
            can_authorize_events=True,
        )

    def create_announcement(self, status=Announcement.Status.DRAFT):
        return Announcement.objects.create(
            tenant=self.tenant,
            school=self.school,
            academic_year=self.academic_year,
            title='Comunicado de teste',
            body='Mensagem para famílias.',
            status=status,
        )

    def create_thread(self):
        return MessageThread.objects.create(
            tenant=self.tenant,
            school=self.school,
            student=self.student,
            guardian=self.guardian,
            subject='Dúvida da família',
        )

    def create_authorization_request(self):
        return AuthorizationRequest.objects.create(
            tenant=self.tenant,
            school=self.school,
            student=self.student,
            title='Autorização de passeio',
            description='Passeio pedagógico.',
            request_type=AuthorizationRequest.RequestType.FIELD_TRIP,
            due_at=timezone.now() + timezone.timedelta(days=7),
        )

    def test_publish_announcement(self):
        announcement = self.create_announcement()

        announcement.publish()

        self.assertEqual(announcement.status, Announcement.Status.PUBLISHED)
        self.assertIsNotNone(announcement.published_at)

    def test_announcement_audience_requires_target_for_class_group(self):
        announcement = self.create_announcement()
        audience = AnnouncementAudience(
            tenant=self.tenant,
            announcement=announcement,
            audience_type=AnnouncementAudience.AudienceType.CLASS_GROUP,
        )

        with self.assertRaises(ValidationError):
            audience.full_clean()

    def test_announcement_read_receipt_requires_reader(self):
        announcement = self.create_announcement(status=Announcement.Status.PUBLISHED)
        receipt = AnnouncementReadReceipt(
            tenant=self.tenant,
            announcement=announcement,
            channel=AnnouncementReadReceipt.Channel.PORTAL,
        )

        with self.assertRaises(ValidationError):
            receipt.full_clean()

    def test_create_guardian_read_receipt(self):
        announcement = self.create_announcement(status=Announcement.Status.PUBLISHED)
        receipt = AnnouncementReadReceipt.objects.create(
            tenant=self.tenant,
            announcement=announcement,
            guardian=self.guardian,
            channel=AnnouncementReadReceipt.Channel.APP,
        )

        self.assertEqual(receipt.channel, AnnouncementReadReceipt.Channel.APP)

    def test_message_thread_close(self):
        thread = self.create_thread()

        thread.close()

        self.assertEqual(thread.status, MessageThread.Status.CLOSED)
        self.assertIsNotNone(thread.closed_at)

    def test_message_requires_sender(self):
        thread = self.create_thread()
        message = Message(tenant=self.tenant, thread=thread, body='Mensagem sem remetente.')

        with self.assertRaises(ValidationError):
            message.full_clean()

    def test_message_mark_read(self):
        thread = self.create_thread()
        message = Message.objects.create(
            tenant=self.tenant,
            thread=thread,
            sender_guardian=self.guardian,
            body='Mensagem da família.',
        )

        message.mark_read()

        self.assertTrue(message.is_read)

    def test_authorization_response_requires_authorized_guardian(self):
        unauthorized_guardian = Guardian.objects.create(
            tenant=self.tenant,
            school=self.school,
            full_name='Responsável sem autorização',
        )
        GuardianStudentLink.objects.create(
            tenant=self.tenant,
            guardian=unauthorized_guardian,
            student=self.student,
            relationship=GuardianStudentLink.Relationship.FATHER,
            can_authorize_events=False,
        )
        request = self.create_authorization_request()
        response = AuthorizationResponse(
            tenant=self.tenant,
            request=request,
            guardian=unauthorized_guardian,
            response=AuthorizationResponse.Response.APPROVED,
        )

        with self.assertRaises(ValidationError):
            response.full_clean()

    def test_authorization_response_approved_for_authorized_guardian(self):
        request = self.create_authorization_request()
        response = AuthorizationResponse(
            tenant=self.tenant,
            request=request,
            guardian=self.guardian,
            response=AuthorizationResponse.Response.APPROVED,
        )

        response.full_clean()
        response.save()

        self.assertEqual(response.response, AuthorizationResponse.Response.APPROVED)
