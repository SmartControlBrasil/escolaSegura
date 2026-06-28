# API v1

Base: `/api/v1/`

## Autenticação

```http
POST /api/v1/auth/token/
username=admin&password=admin123
```

Use o token retornado:

```http
Authorization: Token <token>
```

## Principais rotas

- `/api/v1/core/organizations/`
- `/api/v1/accounts/users/`
- `/api/v1/customers/`
- `/api/v1/catalog/categories/`
- `/api/v1/catalog/products/`
- `/api/v1/catalog/product-items/`
- `/api/v1/inventory/locations/`
- `/api/v1/inventory/balances/`
- `/api/v1/inventory/movements/`
- `/api/v1/sales/orders/`
- `/api/v1/finance/receivables/`
- `/api/v1/finance/payables/`
- `/api/v1/agents/livia/sessions/`
- `/api/v1/agents/atlas/prospects/`
- `/api/v1/policy/data-processing/`
- `/api/v1/policy/incidents/`
- `/api/v1/pages/`

## Orçamentos e vistorias

Endpoints adicionados:

- `GET/POST /api/v1/estimates/estimates/`
- `GET/PUT/PATCH/DELETE /api/v1/estimates/estimates/{id}/`
- `POST /api/v1/estimates/estimates/{id}/recalculate/`
- `POST /api/v1/estimates/estimates/{id}/generate-contact-message/`
- `POST /api/v1/estimates/estimates/{id}/mark-sent/`
- `GET/POST /api/v1/estimates/estimate-lines/`
- `GET/POST /api/v1/estimates/estimate-photos/`
- `GET/POST /api/v1/estimates/estimate-measurements/`
- `GET/POST /api/v1/estimates/estimate-contact-messages/`

Uploads de fotos devem usar `multipart/form-data`.

## Relatórios de serviço

Endpoints adicionados:

- `GET/POST /api/v1/service-reports/reports/`
- `GET/PUT/PATCH/DELETE /api/v1/service-reports/reports/{id}/`
- `POST /api/v1/service-reports/reports/{id}/complete/`
- `GET/POST /api/v1/service-reports/report-items/`
- `GET/POST /api/v1/service-reports/report-photos/`

## Imagens de produtos

Endpoint adicionado:

- `GET/POST /api/v1/catalog/product-images/`

Uploads de imagens de produto também usam `multipart/form-data`.
