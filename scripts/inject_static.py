import os
import re

def process_file(filepath, app_prefix, static_dirs):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if '{% load static %}' not in content:
        content = '{% load static %}\n' + content

    dirs_pattern = '|'.join(static_dirs)
    
    # Replace href="css/..." and src="js/..."
    pattern_attr = re.compile(rf'(href|src)="((?:{dirs_pattern})/[^"]+)"')
    content = pattern_attr.sub(rf'\1="{{% static \'{app_prefix}/\2\' %}}"', content)
    
    # Replace url('image/...') or url("image/...")
    pattern_url = re.compile(rf'url\(([\'"])((?:{dirs_pattern})/[^\'"]+)\1\)')
    content = pattern_url.sub(rf'url({{% static \'{app_prefix}/\2\' %}})', content)
    
    # Replace url(image/...) without quotes
    pattern_url_no_quote = re.compile(rf'url\(((?:{dirs_pattern})/[^\'"]+)\)')
    content = pattern_url_no_quote.sub(rf'url("{{% static \'{app_prefix}/\1\' %}}")', content)

    # Some templates have standard href="index.html" etc. For this basic routing we will map them:
    if app_prefix == 'public_site':
        content = re.sub(r'href="index(-[23])?\.html"', 'href="/"', content)
        content = re.sub(r'href="about\.html"', 'href="/sobre/"', content)
        content = re.sub(r'href="service-list\.html"', 'href="/servicos/"', content)
        content = re.sub(r'href="project\.html"', 'href="/projetos/"', content)
        content = re.sub(r'href="blog-list\.html"', 'href="/blog/"', content)
        content = re.sub(r'href="contact\.html"', 'href="/contato/"', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

public_site_files = [
    'index.html', 'about.html', 'service-list.html', 
    'project.html', 'blog-list.html', 'contact.html'
]
public_site_dir = '/home/marcelo/projetos/Marmoraria_Santander/Santander/templates/public_site'

for pf in public_site_files:
    process_file(os.path.join(public_site_dir, pf), 'public_site', ['css', 'image', 'js', 'scss'])

backoffice_files = ['index.html']
backoffice_dir = '/home/marcelo/projetos/Marmoraria_Santander/Santander/templates/backoffice'

for bf in backoffice_files:
    process_file(os.path.join(backoffice_dir, bf), 'backoffice', ['assets'])

print("Done.")
