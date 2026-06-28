# Arquitetura

A base usa uma abordagem pragmática de DDD + arquitetura hexagonal dentro do ecossistema Django.

Cada app segue a intenção:

```text
apps/<modulo>/
  domain/          # conceitos, entidades conceituais, contratos
  application/     # serviços de aplicação e casos de uso
  infrastructure/  # models Django, persistência e adapters
  interfaces/      # serializers, viewsets, urls
```

O Django Admin e o DRF ficam na borda. O domínio não deve importar views, serializers ou templates.

## Bounded contexts

- Core: organização, configurações, auditoria, anexos.
- Accounts: usuários, perfis e acesso.
- Customers: clientes, contatos e endereços.
- Catalog: categorias, produtos e itens de produtos.
- Inventory: locais, saldos e movimentações.
- Finance: contas a pagar e receber.
- Agents: Lívia, Atlas e base de agentes.
- Policy Guard: LGPD, segurança, consentimento e incidentes.
- Integrations: provedores e webhooks.
- Pages: páginas HTML por nicho.
