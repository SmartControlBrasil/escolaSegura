# Baseline de Segurança e LGPD - EscolaSegura

Este documento apresenta a fundamentação inicial de segurança, conformidade de dados e proteção de usuários estabelecida no projeto EscolaSegura.

## 1. Segurança de Credenciais & Ambiente (`.env`)

Para evitar a exposição de senhas e credenciais fixas (como `admin/admin123`) no código ou repositório:
- O arquivo `.env` gerencia credenciais de banco de dados, chaves de criptografia e usuários de demonstração.
- O arquivo `.env.example` lista todas as variáveis de ambiente obrigatórias:
  * `DJANGO_SUPERUSER_USERNAME` / `DJANGO_SUPERUSER_PASSWORD` (para suporte e administração nativa em `/admin/`)
  * `DEMO_OWNER_USERNAME` / `DEMO_OWNER_PASSWORD` (para a conta de demonstração do painel `/app/`)

### Comandos de Inicialização Segura
Sempre que a aplicação for iniciada em um novo ambiente ou as credenciais do `.env` forem atualizadas, o seguinte comando deve ser executado para configurar os usuários de demonstração no banco de dados com segurança (a senha nunca é exibida no console):

```bash
python manage.py bootstrap_demo_users
```

## 2. Grupos e Controle de Acesso
Definimos grupos/perfis específicos para as funções da escola, organizando o controle de acesso de maneira granular:
* **Proprietário**: Acesso completo ao cockpit e todas as configurações.
* **Comercial**: Criação e acompanhamento de orçamentos e gerenciamento de leads.
* **Técnico**: Acesso a relatórios de vistoria técnica e medições milimétricas de obras.
* **Financeiro**: Acompanhamento de faturamentos de orçamentos aprovados.
* **Admin Técnico**: Controle de infraestrutura técnica geral (Django Admin).

O usuário demonstrativo padrão (`fabrizio`) é automaticamente associado ao grupo **Proprietário**.

## 3. Segurança de Sessão, Cookies e Força Bruta

### Produção (`prod.py`)
Garantimos parâmetros estritamente seguros para cookies de sessão e CSRF em ambientes produtivos:
* `SESSION_COOKIE_SECURE = True` e `CSRF_COOKIE_SECURE = True`
* `SESSION_COOKIE_HTTPONLY = True` e `CSRF_COOKIE_HTTPONLY = True`
* `SESSION_COOKIE_SAMESITE = 'Lax'` e `CSRF_COOKIE_SAMESITE = 'Lax'`
* `SECURE_SSL_REDIRECT = True`
* `SECURE_HSTS_SECONDS = 31536000` (com subdomínios e pré-carregamento)
* `SECURE_CONTENT_TYPE_NOSNIFF = True`
* `X_FRAME_OPTIONS = 'DENY'`

### Proteção Contra Força Bruta
- Integramos a biblioteca `django-axes` configurada para bloquear contas após **5 tentativas falhas sucessivas** de login.
- O tempo padrão de bloqueio temporário (*cooloff*) é de 1 hora.
- Em caso de bloqueio, o formulário de login retorna erros claros de segurança.

## 4. Conformidade LGPD e Auditoria

### Termos e Consentimento no Site Público
- Criamos as páginas `/privacidade/` e `/termos/` contendo textos profissionais e objetivos sobre retenção de dados, direitos do titular e bases legais de acordo com a LGPD.
- O formulário de contato em `/contato/` agora possui um **checkbox de consentimento explícito e obrigatório**:
  > *"Li e aceito a Política de Privacidade e autorizo o contato para atendimento da minha solicitação."*
- Ao preencher o formulário, criamos um registro na tabela `PrivacyConsentLog` salvando com precisão o IP, User Agent, Dados de Contato e a data/hora para auditoria posterior.

### Auditoria de Ações Sensíveis (`ActivityLog`)
Eventos importantes são registrados na tabela de auditoria da base de dados (`ActivityLog`), permitindo rastreabilidade:
- Login bem-sucedido.
- Tentativas de login inválidas (com dados de usuário preservados sem salvar a senha).
- Logout da sessão.
- Criação de novos orçamentos no painel comercial.
