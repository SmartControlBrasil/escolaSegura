from django.shortcuts import render

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
    return render(request, 'public_site/contact.html')
