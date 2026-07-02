# Como evoluir por nicho

Para criar um sistema derivado:

1. Clone a base.
2. Ajuste nome, domínio e `.env`.
3. Preserve Core, Accounts, Policy Guard e Integrations.
4. Escolha os módulos do nicho.
5. Crie novos apps seguindo o padrão:

```bash
apps/<novo_modulo>/domain
apps/<novo_modulo>/application
apps/<novo_modulo>/infrastructure
apps/<novo_modulo>/interfaces
```

6. Só depois integre HTML/template.

## Exemplos de módulos futuros

- WorkOrders: ordens de serviço.
- Scheduling: agenda técnica.
- Contracts: contratos e recorrência.
- Sales: propostas e pedidos.
- Purchasing: compras e fornecedores.
- Ecommerce: catálogo público, carrinho e pedidos online.
- Reports: indicadores e BI.

## Camada de orçamento e serviço em campo

Para derivar um sistema por nicho, reaproveite:

- `Catalog.Product` e `Catalog.ProductImage` para catálogo visual;
- `Estimates.Estimate` para proposta/orçamento;
- `Estimates.EstimatePhoto` para vistoria técnica;
- `Estimates.EstimateMeasurement` para levantamento de medidas;
- `ServiceReports.ServiceReport` para entrega/execução;
- `ServiceReports.ServiceReportPhoto` para evidências de serviço.

Exemplos:

- escola: medidas, fotos de bancada, recortes, cuba, acabamento;
- ar-condicionado: fotos do ambiente, evaporadora/condensadora, distância, dreno;
- obra civil: antes/depois, materiais, metragem, etapas;
- manutenção industrial: evidências técnicas, componentes, diagnóstico, relatório.
