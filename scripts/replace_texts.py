import os
import glob

directory = "/home/marcelo/projetos/Escola_EscolaSegura/EscolaSegura/templates/public_site/"
files = glob.glob(os.path.join(directory, "*.html"))

replacements = {
    # Nav/Footer generic terms
    "Home": "Início",
    "About Us": "Empresa",
    "Our Services": "Nossos Serviços",
    "Services": "Serviços",
    "Projects": "Projetos",
    "Project": "Projetos",
    "Blog": "Notícias",
    "Contact Us": "Contato",
    "Contact": "Contato",
    "Get A Quote": "Faça um Orçamento",
    "Read More": "Saiba Mais",
    "View Details": "Ver Detalhes",
    
    # Company Name and Info
    "Intereal": "EscolaSegura",
    "121 King Street, Melbourne Victoria 3000 Australia": "São Paulo - SP",
    "info@example.com": "comercial@santanderescola.com.br",
    "(+01) 123 456 7890": "(11) 4142-1413 / (11) 98271-9989",
    "Architecture": "Mármore",
    "Interior Design": "Granito",
    "3D Modeling": "Silestone",
    
    # Specific texts
    "We provide the best": "Serviço Com Alto",
    "Architecture & Interior Design": "Padrão de Qualidade EscolaSegura!",
    "Ready To Start New Project With": "Pronto para Iniciar seu Projeto com a",
    "We Will Make Your": "Nós Faremos o Seu",
    "Dream Come True": "Sonho se Tornar Realidade",
    
    # Forms
    "First Name": "Nome",
    "Last Name": "Sobrenome",
    "Email Address": "E-mail",
    "Write Message": "Escreva sua Mensagem",
    "Send Message": "Enviar Mensagem",
    
    # about.html specific (we will just inject the mission/vision in the first big lorem ipsum)
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.": "Conheça um pouquinho mais sobre nós!\n\n<b>MISSÃO:</b> Atender todas às demandas de nossos clientes a partir do desenvolvimento e oferta de produtos e serviços que contribuam para a melhoria da qualidade de vida das pessoas, gerando riqueza de forma sustentável.\n<br><br>\n<b>VISÃO:</b> Ser empresa de referência, reconhecida como a melhor opção por clientes, colaboradores, comunidade, fornecedores e investidores, devido à qualidade de nossos produtos, serviços e relacionamento.\n<br><br>\n<b>VALORES:</b> Integridade, Comprometimento, Valorização Humana, Superação de Resultados, Melhoria contínua, Inovação, Sustentabilidade."
}

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for old, new in replacements.items():
        content = content.replace(old, new)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Text replaced.")
