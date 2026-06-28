# Smart System Base — Django / Postgres / DDD Hexagonal

Base reutilizável para criação de sistemas administrativos, ERPs leves, CRMs operacionais, portais com IA e automações comerciais.

Esta base foi pensada para servir como **produto-base** e não como protótipo. Ela nasce com backend estruturado, API REST, Django Admin, Postgres, módulos de negócio e camada de agentes preparada para evolução.

## O que já vem pronto

- Django com configuração separada por ambiente.
- Banco Postgres.
- Django Admin operacional.
- API REST versionada em `/api/v1/`.
- Autenticação por token do Django REST Framework.
- Estrutura modular inspirada em DDD + arquitetura hexagonal.
- Cadastro de organizações, filiais, usuários e configurações.
- Cadastro de clientes, contatos e endereços.
- Cadastro de categorias, produtos e itens de produtos.
- Estoque com locais, saldos e movimentações.
- Vendas com pedidos e itens de pedido.
- Financeiro com contas a pagar e receber.
- Base de assistente virtual estilo Lívia.
- Base de prospecção/Atlas com revisão humana antes de e-mail.
- Agente de política, LGPD e segurança da informação.
- Módulo de páginas HTML desacoplado por nicho.
- Documentação para deploy em VPS HostGator/CyberPanel.

## Stack

- Python 3.12+
- Django 6.x
- Django REST Framework
- PostgreSQL
- Gunicorn
- WhiteNoise
- CyberPanel/OpenLiteSpeed na VPS

## Setup local rápido

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_base
python manage.py runserver
```

## Rotas principais

- Admin: `/admin/`
- API root: `/api/v1/`
- Healthcheck: `/api/v1/health/`
- Login token: `/api/v1/auth/token/`

## Filosofia

A regra é simples: **o domínio não deve depender da interface**. Templates HTML, painéis, vitrines e páginas públicas entram depois, conforme o projeto do cliente.

A base entrega o motor. A lataria muda por nicho.


## Orçamentos, vistorias e relatórios de serviço

A base inclui módulos prontos para serviços em campo:

- `apps.estimates`: orçamentos editáveis, itens, fotos de vistoria, medições e mensagem de primeiro contato.
- `apps.service_reports`: relatórios de serviço, evidências fotográficas, itens executados e conclusão.
- `ProductImage`: imagens de produtos no catálogo.
- UI HTML base em `/app/estimates/` e `/app/service-reports/`.

O profissional pode abrir a vistoria no celular e capturar fotos diretamente pelo navegador usando campos de upload com `accept="image/*"` e `capture="environment"`.
