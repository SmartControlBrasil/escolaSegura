# Orçamentos, Vistorias Mobile e Relatórios de Serviço

Esta base agora inclui uma camada operacional forte para empresas de serviço: escolas, instaladores de ar-condicionado, manutenção industrial, pedreiros, elétrica, refrigeração, assistência técnica e outros nichos.

## Módulo Estimates

O módulo `apps.estimates` cobre:

- orçamento editável;
- itens de orçamento;
- fotos de vistoria;
- medições;
- mensagem de primeiro contato;
- fluxo de status do orçamento;
- API REST;
- telas HTML base para dashboard, editor e vistoria mobile.

### Fluxo canônico

1. Cliente solicita orçamento.
2. Usuário cria um `Estimate`.
3. Sistema gera mensagem inicial para WhatsApp/e-mail.
4. Profissional abre `/app/estimates/<id>/vistoria/` no celular.
5. Tira fotos da obra/ambiente pelo input `capture="environment"`.
6. Registra medidas e observações.
7. Usa fotos, medidas e itens para montar a proposta.
8. Orçamento é enviado/aprovado.

## Módulo Service Reports

O módulo `apps.service_reports` cobre:

- relatório de serviço;
- itens executados/cobráveis;
- fotos antes/durante/depois;
- evidências técnicas;
- conclusão de atendimento;
- API REST;
- telas HTML base para relatórios.

## UI

A UI foi feita sem acoplar tema específico. Ela fica em:

- `templates/app_base.html`
- `templates/estimates/*`
- `templates/service_reports/*`
- `static/css/smart_system_ui.css`

Essa UI é propositalmente neutra e forte o bastante para servir como base. Cada projeto derivado pode trocar a identidade visual depois.

## Endpoints principais

- `/api/v1/estimates/estimates/`
- `/api/v1/estimates/estimate-lines/`
- `/api/v1/estimates/estimate-photos/`
- `/api/v1/estimates/estimate-measurements/`
- `/api/v1/estimates/estimate-contact-messages/`
- `/api/v1/service-reports/reports/`
- `/api/v1/service-reports/report-items/`
- `/api/v1/service-reports/report-photos/`

## Rotas HTML base

- `/app/estimates/`
- `/app/estimates/builder/`
- `/app/estimates/builder/<uuid>/`
- `/app/estimates/<uuid>/vistoria/`
- `/app/service-reports/`
- `/app/service-reports/<uuid>/`
