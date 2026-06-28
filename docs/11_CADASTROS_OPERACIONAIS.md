# Cadastros Operacionais Marmoraria360

Esta documentação descreve a fundação completa do CRM e ERP do produto Marmoraria360, focada na gestão operacional da marmoraria.

## Arquitetura de Dados Implementada

Para suportar as telas demonstrativas sem quebrar a estrutura existente, expandimos o banco de dados e adicionamos novos modelos alinhados aos princípios de DDD:

1. **Clientes** (`customers.Customer`):
   - Foram adicionados: `whatsapp`, `address`, `lead_origin`, `lgpd_consent`.

2. **Catálogo / Produtos** (`catalog.Product`):
   - Foram adicionados: `cost_price` (custo), `suggested_margin` (margem sugerida), `supplier` (fornecedor), `image` (imagem do produto).

3. **Orçamentos** (`estimates.Estimate`):
   - Foram adicionados: `environment` (ambiente), `deadline_days` (prazo em dias).

4. **Vistorias** (`service_reports.ServiceReport`):
   - Foram adicionados: `scheduled_date` (data agendada), `risks_reported` (riscos mapeados).

5. **Entregas de Obra** (`service_reports.ProjectDelivery`):
   - **Novo modelo** gerencia o checklist de entrega técnica, conectando o Cliente à Obra.

6. **Obras / Projetos** (`sales.Project`):
   - **Novo modelo** representa a obra aprovada e sua fase produtiva/instalação.

7. **Fornecedores** (`core.Supplier`):
   - **Novo modelo** centralizando insumos, ferramentas e chapas, conectados aos produtos.

8. **Veículos** (`core.Vehicle`):
   - **Novo modelo** para controle de frota (Fiorino, HR, etc) para as Entregas e Vistorias.

9. **Financeiro** (`finance.AccountPayable` e `finance.AccountReceivable`):
   - Exposição na interface de Contas a Pagar e Receber.

10. **Usuários** (`accounts.User`):
    - Gestão simplificada para alocação de usuários e grupos (Administrador, Técnico, Comercial).

## Camada de Apresentação (Views & Templates)

Todas as views foram alocadas em `apps/backoffice/views.py` seguindo o padrão de rotas protegidas pelo `@login_required`.

- As rotas `/app/X/` listam os registros (List View).
- As rotas `/app/X/novo/` criam novos registros (Create View).
- As rotas `/app/X/<uuid:id>/` mostram os detalhes e permitem edição (Update View).

### Clonagem Produtiva de Templates

Os templates foram gerados com base na anatomia robusta do template Intereal/Skodash (`clientes.html`, `clientes_novo.html`, `clientes_detalhe.html`), usando scripts de automatização para manter a coerência visual exata desejada pelo cliente. As classes CSS, JS e HTML base originais foram preservadas.

## População de Dados (Seed)

O comando `python manage.py seed_marmoraria_demo` foi atualizado para criar não apenas Orçamentos e Clientes, mas injetar dados realistas em **Obras, Fornecedores, Veículos, Entregas e Financeiro**. Essa atualização garante que, ao apresentar o software para uma marmoraria real, o painel pareça estar em uso pleno (Growth Engine, IA, Obras em Andamento, Contas a Pagar, etc).

## Limitações Atuais
- **Validações de Domínio:** Os formulários atualmente não possuem bloqueios avançados de regras de negócio (ex: não é possível bloquear a exclusão de um cliente se ele possuir orçamentos abertos, pois a operação de exclusão ainda não foi disponibilizada).
- **Relatórios:** A tela de relatórios exibe apenas dados consolidados estáticos, sem paginação nativa e gráficos interativos reais consumindo JSON assíncrono.
- **Uploads:** O upload de imagens demonstrativas em "Catálogo" ainda não possui processamento em S3/CDN.

## Próximos Passos
1. Implementar `DeleteView` com verificação de constraints em todos os CRUDs.
2. Adicionar filtros e paginação nativa (usando Django Pagination) nas telas de listagem.
3. Consolidar Dashboards reais utilizando Chart.js consumindo a API.
