import os

base_path = '/home/marcelo/projetos/Marmoraria_Santander/Santander/templates/backoffice/base.html'
index_path = '/home/marcelo/projetos/Marmoraria_Santander/Santander/templates/backoffice/index.html'

with open(base_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 1. Extract dashboard content (lines 746 to 1613, which is lines[745:1613] 0-indexed)
dashboard_content = "".join(lines[745:1613])

# 2. Modify menu and tab content in base.html
# Let's rebuild the file using chunks.
# The sidebar-left nav is around lines[492:542] (0-indexed: line 493 to 542)
# The tab-content is around lines[547:739] (0-indexed: line 548 to 739)
# The main content is lines[745:1613]

part1 = "".join(lines[:492])

new_nav = """            <ul class="nav nav-pills flex-column">
              <li class="nav-item" data-bs-toggle="tooltip" data-bs-placement="right" title="Dashboard">
                <button class="nav-link active" data-bs-toggle="pill" data-bs-target="#pills-dashboards" type="button"><i class="bi bi-house-door-fill"></i></button>
              </li>
              <li class="nav-item" data-bs-toggle="tooltip" data-bs-placement="right" title="Marmoraria360">
                <button class="nav-link" data-bs-toggle="pill" data-bs-target="#pills-marmoraria" type="button"><i class="bi bi-tools"></i></button>
              </li>
              <li class="nav-item" data-bs-toggle="tooltip" data-bs-placement="right" title="IA & Growth">
                <button class="nav-link" data-bs-toggle="pill" data-bs-target="#pills-growth" type="button"><i class="bi bi-cpu"></i></button>
              </li>
              <li class="nav-item" data-bs-toggle="tooltip" data-bs-placement="right" title="Configurações">
                <button class="nav-link" data-bs-toggle="pill" data-bs-target="#pills-settings" type="button"><i class="bi bi-gear-fill"></i></button>
              </li>
            </ul>"""

part2 = "".join(lines[542:548])

new_tabs = """            <div class="tab-content">
              <div class="tab-pane fade show active" id="pills-dashboards">
                <div class="list-group list-group-flush">
                  <div class="list-group-item">
                    <div class="d-flex w-100 justify-content-between">
                      <h5 class="mb-0">Dashboard</h5>
                    </div>
                    <small class="mb-0">Painel Principal</small>
                  </div>
                  <a href="/app/" class="list-group-item"><i class="bi bi-house-door"></i>Início</a>
                </div>
              </div>
              <div class="tab-pane fade" id="pills-marmoraria">
                <div class="list-group list-group-flush">
                  <div class="list-group-item">
                    <div class="d-flex w-100 justify-content-between">
                      <h5 class="mb-0">Marmoraria360</h5>
                    </div>
                    <small class="mb-0">Gestão Comercial</small>
                  </div>
                  <a href="/app/clientes/" class="list-group-item"><i class="bi bi-people"></i>Clientes</a>
                  <a href="/app/catalogo/" class="list-group-item"><i class="bi bi-journal-text"></i>Catálogo</a>
                  <a href="/app/orcamentos/" class="list-group-item"><i class="bi bi-file-earmark-ruled"></i>Orçamentos</a>
                  <a href="/app/vistorias/" class="list-group-item"><i class="bi bi-clipboard-check"></i>Vistorias</a>
                  <a href="/app/relatorios/" class="list-group-item"><i class="bi bi-graph-up"></i>Relatórios</a>
                </div>
              </div>
              <div class="tab-pane fade" id="pills-growth">
                <div class="list-group list-group-flush">
                  <div class="list-group-item">
                    <div class="d-flex w-100 justify-content-between">
                      <h5 class="mb-0">IA & Growth</h5>
                    </div>
                    <small class="mb-0">Crescimento Acelerado</small>
                  </div>
                  <a href="#" class="list-group-item"><i class="bi bi-lightning"></i>Growth Engine</a>
                  <a href="#" class="list-group-item"><i class="bi bi-compass"></i>Atlas</a>
                  <a href="#" class="list-group-item"><i class="bi bi-robot"></i>Assistente Virtual</a>
                </div>
              </div>
              <div class="tab-pane fade" id="pills-settings">
                <div class="list-group list-group-flush">
                  <div class="list-group-item">
                    <div class="d-flex w-100 justify-content-between">
                      <h5 class="mb-0">Configurações</h5>
                    </div>
                    <small class="mb-0">Opções do Sistema</small>
                  </div>
                  <a href="#" class="list-group-item"><i class="bi bi-gear"></i>Configurações</a>
                </div>
              </div>
            </div>"""

part3 = "".join(lines[739:745])

new_content = "        {% block content %}\n        {% endblock %}"

part4 = "".join(lines[1613:])

# Save modified base.html
with open(base_path, 'w', encoding='utf-8') as f:
    f.write(part1 + "\n" + new_nav + "\n" + part2 + "\n" + new_tabs + "\n" + part3 + "\n" + new_content + "\n" + part4)

# Overwrite index.html to extend base.html
new_index = f"""{{% extends 'backoffice/base.html' %}}
{{% block content %}}
{dashboard_content}
{{% endblock %}}"""

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(new_index)

print("Backoffice templates restructured successfully.")
