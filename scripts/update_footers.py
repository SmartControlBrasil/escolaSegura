import os
import glob

directory = "/home/marcelo/projetos/Escola_EscolaSegura/EscolaSegura/templates/public_site/"
files = glob.glob(os.path.join(directory, "*.html"))

for filepath in files:
    # Skip our new privacy and terms pages
    if "privacy.html" in filepath or "terms.html" in filepath:
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace Policies link
    old_policies = '<li><a href="">Policies</a></li>'
    new_policies = '<li><a href="/privacidade/">Privacidade</a></li>\n                  <li><a href="/termos/">Termos de Uso</a></li>'
    
    content = content.replace(old_policies, new_policies)
    
    # Replace support/info emails and phone numbers to match our corporate profile
    content = content.replace("info@website.com", "comercial@santanderescola.com.br")
    content = content.replace("info@intereal.com", "comercial@santanderescola.com.br")
    content = content.replace("support@intereal.com", "comercial@santanderescola.com.br")
    content = content.replace("+33 877 554 332", "(11) 4142-1413 / (11) 98271-9989")
    content = content.replace("+569 2316 2156", "(11) 4142-1413 / (11) 98271-9989")
    content = content.replace("256 Elizaberth Ave, CA, 90025", "São Paulo - SP")
    content = content.replace("256 Elizaberth Ave, <br> CA, 90025", "São Paulo - SP")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Footers and contacts updated across all public pages.")
