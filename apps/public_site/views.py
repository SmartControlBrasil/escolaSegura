from django.shortcuts import render, redirect
from apps.policy_guard.models import PrivacyConsentLog

def home(request):
    return render(request, 'public_site/index.html')

def about(request):
    return render(request, 'public_site/about.html')

def services(request):
    return render(request, 'public_site/service-list.html')

def projects(request):
    return render(request, 'public_site/project.html')

def blog(request):
    return render(request, 'public_site/blog-list.html')

def contact(request):
    success = request.GET.get('success', '') == '1'
    if request.method == 'POST':
        full_name = request.POST.get('full-name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        message = request.POST.get('message', '')
        consent = request.POST.get('lgpd_consent') == 'on'
        
        if full_name and email and consent:
            # Extract IP
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            
            PrivacyConsentLog.objects.create(
                name=full_name,
                email=email,
                phone=phone,
                source='contato',
                consent_text='Li e aceito a Política de Privacidade e autorizo o contato para atendimento da minha solicitação.',
                ip_address=ip,
                user_agent=user_agent
            )
            return redirect('/contato/?success=1')
            
    context = {
        'success': success
    }
    return render(request, 'public_site/contact.html', context)

def privacy(request):
    return render(request, 'public_site/privacy.html')

def terms(request):
    return render(request, 'public_site/terms.html')
