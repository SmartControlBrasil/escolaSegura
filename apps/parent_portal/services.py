from django.shortcuts import get_object_or_404

from apps.guardians.models import Guardian, GuardianStudentLink
from apps.students.models import StudentEnrollment


def get_guardian_for_user(user):
    if not getattr(user, 'is_authenticated', False) or not user.email:
        return None
    return Guardian.objects.filter(email__iexact=user.email, is_active=True).first()


def get_active_links_for_user(user):
    guardian = get_guardian_for_user(user)
    if guardian is None:
        return guardian, GuardianStudentLink.objects.none()
    links = (
        GuardianStudentLink.objects
        .filter(guardian=guardian, is_active=True, student__is_active=True)
        .select_related('student', 'student__school', 'tenant')
        .order_by('student__full_name')
    )
    return guardian, links


def get_linked_student_or_404(user, student_id):
    guardian = get_guardian_for_user(user)
    link = get_object_or_404(
        GuardianStudentLink.objects.select_related('student', 'student__school'),
        guardian=guardian,
        student_id=student_id,
        is_active=True,
    )
    return guardian, link.student


def get_current_enrollment(student):
    return (
        StudentEnrollment.objects
        .filter(student=student, status=StudentEnrollment.Status.ACTIVE)
        .select_related('class_group', 'academic_year')
        .order_by('-enrolled_at', '-created_at')
        .first()
    )
