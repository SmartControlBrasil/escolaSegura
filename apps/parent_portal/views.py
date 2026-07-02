from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.db.models import Q, Prefetch
from django.shortcuts import render
from django.templatetags.static import static

from apps.assessments.models import ReportCard
from apps.attendance.models import AttendanceRecord
from apps.communication.models import Announcement, AuthorizationRequest, Message, MessageThread
from apps.students.models import StudentEnrollment

from .services import get_active_links_for_user, get_current_enrollment, get_linked_student_or_404


def _student_context(request, student_id):
    guardian, student = get_linked_student_or_404(request.user, student_id)
    enrollment = get_current_enrollment(student)
    return guardian, student, enrollment


def _published_announcements(student, guardian, enrollment=None):
    filters = Q(audiences__audience_type='ALL_SCHOOL', school=student.school)
    filters |= Q(audiences__audience_type='STUDENT', audiences__student=student)
    filters |= Q(audiences__audience_type='GUARDIAN', audiences__guardian=guardian)
    if enrollment is not None:
        filters |= Q(audiences__audience_type='CLASS_GROUP', audiences__class_group=enrollment.class_group)
    return (
        Announcement.objects
        .filter(status=Announcement.Status.PUBLISHED)
        .filter(filters)
        .select_related('school', 'unit', 'academic_year')
        .distinct()
        .order_by('-published_at', '-created_at')
    )


@login_required
def dashboard(request):
    guardian, links = get_active_links_for_user(request.user)
    students = []
    for link in links:
        student = link.student
        student.current_enrollment = get_current_enrollment(student)
        students.append(student)
    return render(request, 'parent_portal/dashboard.html', {'guardian': guardian, 'students': students})


@login_required
def student_detail(request, student_id):
    guardian, student, enrollment = _student_context(request, student_id)
    attendance_records = (
        AttendanceRecord.objects
        .filter(student=student)
        .select_related('session', 'session__class_group', 'session__subject')
        .order_by('-session__session_date', '-session__session_number')[:5]
    )
    announcements = _published_announcements(student, guardian, enrollment)[:5]
    authorization_requests = (
        AuthorizationRequest.objects
        .filter(student=student, status=AuthorizationRequest.Status.OPEN)
        .order_by('due_at', '-created_at')[:5]
    )
    report_card = (
        ReportCard.objects
        .filter(student=student, status=ReportCard.Status.PUBLISHED)
        .select_related('academic_year', 'term')
        .order_by('-published_at', '-created_at')
        .first()
    )
    context = {
        'guardian': guardian,
        'student': student,
        'enrollment': enrollment,
        'attendance_records': attendance_records,
        'announcements': announcements,
        'authorization_requests': authorization_requests,
        'report_card': report_card,
    }
    return render(request, 'parent_portal/student_detail.html', context)


@login_required
def attendance(request, student_id):
    guardian, student, enrollment = _student_context(request, student_id)
    records = (
        AttendanceRecord.objects
        .filter(student=student)
        .select_related('session', 'session__class_group', 'session__subject')
        .order_by('-session__session_date', '-session__session_number')
    )
    return render(request, 'parent_portal/attendance.html', {
        'guardian': guardian,
        'student': student,
        'enrollment': enrollment,
        'records': records,
    })


@login_required
def announcements(request, student_id):
    guardian, student, enrollment = _student_context(request, student_id)
    items = _published_announcements(student, guardian, enrollment)
    return render(request, 'parent_portal/announcements.html', {
        'guardian': guardian,
        'student': student,
        'enrollment': enrollment,
        'announcements': items,
    })


@login_required
def messages(request, student_id):
    guardian, student, enrollment = _student_context(request, student_id)
    latest_messages = Message.objects.order_by('-sent_at')
    threads = (
        MessageThread.objects
        .filter(Q(guardian=guardian) | Q(student=student), school=student.school)
        .select_related('student', 'guardian')
        .prefetch_related(Prefetch('messages', queryset=latest_messages, to_attr='latest_messages'))
        .order_by('-created_at')
    )
    return render(request, 'parent_portal/messages.html', {
        'guardian': guardian,
        'student': student,
        'enrollment': enrollment,
        'threads': threads,
    })


@login_required
def authorizations(request, student_id):
    guardian, student, enrollment = _student_context(request, student_id)
    requests = (
        AuthorizationRequest.objects
        .filter(student=student)
        .prefetch_related('responses')
        .order_by('-created_at')
    )
    for request_item in requests:
        request_item.guardian_response = next(
            (response for response in request_item.responses.all() if response.guardian_id == guardian.id),
            None,
        )
    return render(request, 'parent_portal/authorizations.html', {
        'guardian': guardian,
        'student': student,
        'enrollment': enrollment,
        'authorization_requests': requests,
    })


@login_required
def report_card(request, student_id):
    guardian, student, enrollment = _student_context(request, student_id)
    report_cards = (
        ReportCard.objects
        .filter(student=student, status=ReportCard.Status.PUBLISHED)
        .select_related('academic_year', 'term')
        .prefetch_related('entries__subject')
        .order_by('-published_at', '-created_at')
    )
    return render(request, 'parent_portal/report_card.html', {
        'guardian': guardian,
        'student': student,
        'enrollment': enrollment,
        'report_cards': report_cards,
    })

PWA_THEME_COLOR = '#0f766e'
PWA_BACKGROUND_COLOR = '#f5f7fb'


def manifest_json(request):
    return JsonResponse({
        'name': 'EscolaSegura Família',
        'short_name': 'EscolaSegura',
        'start_url': '/familia/',
        'scope': '/familia/',
        'display': 'standalone',
        'background_color': PWA_BACKGROUND_COLOR,
        'theme_color': PWA_THEME_COLOR,
        'description': 'Portal mobile EscolaSegura para responsáveis acompanharem alunos, comunicados, autorizações, frequência e boletins.',
        'orientation': 'portrait-primary',
        'icons': [
            {
                'src': static('backoffice/assets/images/favicon-32x32.png'),
                'sizes': '32x32',
                'type': 'image/png',
                'purpose': 'any maskable',
            },
            {
                'src': static('backoffice/assets/images/logo-icon.png'),
                'sizes': '192x192',
                'type': 'image/png',
                'purpose': 'any maskable',
            },
            {
                'src': static('backoffice/assets/images/brand-logo-2.png'),
                'sizes': '512x512',
                'type': 'image/png',
                'purpose': 'any',
            },
        ],
    }, content_type='application/manifest+json')


def service_worker_js(request):
    asset_urls = [
        static('parent_portal/css/parent_portal.css'),
        static('backoffice/assets/images/favicon-32x32.png'),
        static('backoffice/assets/images/logo-icon.png'),
        static('backoffice/assets/images/brand-logo-2.png'),
    ]
    asset_list = ',\n  '.join(repr(url) for url in asset_urls)
    body = f"""const CACHE_NAME = 'escolasegura-familia-assets-v1';
const ASSET_URLS = [
  {asset_list}
];

self.addEventListener('install', (event) => {{
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSET_URLS))
  );
  self.skipWaiting();
}});

self.addEventListener('activate', (event) => {{
  event.waitUntil(
    caches.keys().then((keys) => Promise.all(
      keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))
    ))
  );
  self.clients.claim();
}});

self.addEventListener('fetch', (event) => {{
  const request = event.request;
  const url = new URL(request.url);

  // Segurança: páginas autenticadas não são cacheadas neste service worker.
  // Dados de alunos, responsáveis, boletins, mensagens e autorizações não são armazenados offline neste MVP.
  // O cache é apenas para assets públicos e estáticos listados em ASSET_URLS.
  if (request.mode === 'navigate' || request.headers.get('accept')?.includes('text/html')) {{
    return;
  }}

  if (url.origin !== self.location.origin || !ASSET_URLS.includes(url.pathname)) {{
    return;
  }}

  event.respondWith(
    caches.match(request).then((cachedResponse) => {{
      return cachedResponse || fetch(request).then((networkResponse) => {{
        const copy = networkResponse.clone();
        caches.open(CACHE_NAME).then((cache) => cache.put(request, copy));
        return networkResponse;
      }});
    }})
  );
}});
"""
    response = HttpResponse(body, content_type='application/javascript')
    response['Service-Worker-Allowed'] = '/familia/'
    return response

