# LGPD e Segurança da Informação

Esta base considera segurança e LGPD como fundação.

## Diretrizes aplicadas

- Registro de tratamento de dados.
- Consentimentos rastreáveis.
- Incidentes de segurança.
- Auditoria de ações.
- Configurações sensíveis separadas por `.env`.
- Envio do Atlas em modo dry-run por padrão.
- E-mails de prospecção exigem aprovação humana.

## Antes de produção

- Trocar `DJANGO_SECRET_KEY`.
- Ativar HTTPS.
- Definir `SECURE_SSL_REDIRECT=true`.
- Definir cookies seguros.
- Configurar backups.
- Configurar política de retenção.
- Revisar bases legais de tratamento.
- Remover senhas padrão.
