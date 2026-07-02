# EscolaSegura

Plataforma SaaS de gestão escolar da Smart Control Brasil.

- **Produto:** EscolaSegura
- **Domínio planejado:** escolasegura360.com.br
- **Repositório:** SmartControlBrasil/escolaSegura
- **Aplicação Django:** diretório `app/`

## O que já existe

### Domínio escolar
- `apps.schools` — escolas, unidades e anos letivos
- `apps.students` — alunos e matrículas
- `apps.guardians` — responsáveis e vínculos
- `apps.academics` — estrutura acadêmica
- `apps.attendance` — frequência
- `apps.communication` — comunicados, mensagens e autorizações
- `apps.assessments` — avaliações e boletins
- `apps.parent_portal` — portal da família (`/familia/`)

### SaaS multi-escola
- `apps.saas` — tenants, planos, assinaturas e uso
- Admin Master no backoffice (`/app/saas/`)

### Backoffice e site público
- Backoffice provisório em `/app/` (visual mínimo EscolaSegura)
- Site público provisório em `/` (visual mínimo EscolaSegura)
- Django Admin em `/admin/`

## Próximas etapas visuais

- Site público final com template **Edumim** (`../edumim`)
- Painel administrativo final com template **Akademi** (`../akademi`)

## Comandos úteis

```bash
cd app
.venv/bin/python manage.py check
.venv/bin/python manage.py test
.venv/bin/python manage.py runserver
```

## Seeds de demonstração

- `bootstrap_demo_users` — usuários demo via variáveis de ambiente
- `seed_escola_segura_demo` — dados comerciais legados + módulos escolares de demo
