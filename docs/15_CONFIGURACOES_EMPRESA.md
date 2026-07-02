# Configurações da Empresa (CompanyProfile)

Este documento descreve a funcionalidade de **Configurações da Empresa** no Marmoraria360, detalhando seu propósito, a modelagem dos dados, sua integração com as propostas comerciais e a emissão de PDFs, e as considerações para futura expansão multi-tenant (SaaS).

---

## 1. Objetivo do CompanyProfile

O modelo `CompanyProfile` foi desenvolvido para transformar o Marmoraria360 em uma plataforma reutilizável (**white-label**). Ele permite que qualquer marmoraria configure seus dados cadastrais, marca e regras comerciais diretamente do painel administrativo, eliminando qualquer tipo de texto ou logomarca *hardcoded* nos cabeçalhos, rodapés e termos de documentos.

---

## 2. Campos Disponíveis

Cada perfil de empresa possui as seguintes propriedades cadastráveis:

*   **trade_name** (*Nome Fantasia*): Nome comercial da marmoraria exibido em destaque nos documentos.
*   **legal_name** (*Razão Social*): Nome de registro legal da empresa.
*   **cnpj** (*CNPJ*): Documento identificador da empresa.
*   **phone** (*Telefone*): Telefone fixo ou móvel de atendimento geral.
*   **whatsapp** (*WhatsApp*): Número utilizado para disparos e contatos comerciais rápidos.
*   **email** (*E-mail Comercial*): E-mail de contato oficial para envio de orçamentos.
*   **website** (*Site*): URL da página institucional da empresa.
*   **address** (*Endereço Completo*): Logradouro, número, bairro e complemento da empresa.
*   **city** (*Cidade*): Cidade sede do perfil.
*   **state** (*UF*): Estado sede da empresa (sigla com 2 caracteres).
*   **business_hours** (*Horário de Atendimento*): Texto livre descrevendo dias e horários de funcionamento.
*   **slogan** (*Slogan*): Frase de posicionamento comercial da marca.
*   **logo** (*Logomarca*): Campo de imagem carregado para exibição nos documentos em PDF.
*   **footer_text** (*Texto Padrão de Rodapé*): Mensagem impressa na base de todas as propostas comerciais.
*   **default_terms** (*Condições Comerciais Padrão*): Texto padrão contendo condições de pagamento, prazos de entrega e especificidades sobre pedras naturais.
*   **default_estimate_validity** (*Validade Padrão*): Quantidade de dias padrão para a expiração de propostas comerciais geradas no sistema.
*   **privacy_policy** (*Política de Privacidade*): Políticas de retenção e tratamento de dados adequados à LGPD.
*   **terms_of_use** (*Termos de Uso*): Termos de uso contratuais.
*   **is_active** (*Cadastro Ativo*): Flag booleana controlando a atividade do perfil.

---

## 3. Mecanismo de Fallback Seguro (Null Object Pattern)

Para garantir que a exclusão ou ausência de um `CompanyProfile` nunca cause falhas críticas na renderização das telas ou na emissão de arquivos PDF, o sistema adota o padrão de **Fallback Seguro**:

1.  O modelo `Organization` possui a propriedade `@property company_profile`.
2.  Caso o relacionamento 1-para-1 `profile` não exista ou esteja corrompido, a propriedade captura a exceção e retorna dinamicamente uma instância de `FallbackCompanyProfile`.
3.  O `FallbackCompanyProfile` simula todos os atributos de um perfil de empresa padrão, utilizando dados demonstrativos pré-definidos (Marmoraria Santander).
4.  Dessa forma, os templates HTML executam `organization.company_profile.trade_name` de forma transparente, eliminando a necessidade de validações condicionais complexas no código de visualização.

---

## 4. Impacto nos PDFs e Documentos Comerciais

Os dados cadastrados em `CompanyProfile` refletem diretamente em:

*   **Preview de Orçamentos (`/app/orcamentos/<id>/preview/`)**: O cabeçalho carrega a logomarca do perfil (se houver) ou o nome fantasia estilizado, o CNPJ e o endereço comercial completo dinamicamente. O rodapé de termos e condições exibe as regras de pagamento salvas no perfil.
*   **PDF de Orçamentos (`/app/orcamentos/<id>/pdf/`)**: O arquivo gerado via `weasyprint` é atualizado na mesma estrutura, garantindo a uniformidade da proposta impressa.
*   **PDF de Termo de Entrega (`/app/entregas/<id>/pdf/`)**: Os dados do emissor (marmoraria responsável técnica) são alterados no termo físico e no bloco de assinatura final, onde o nome fantasia do perfil substitui referências estáticas.

---

## 5. Próximos Passos para Multiempresa e SaaS

Embora a versão atual atenda a uma única empresa (vinculando 1-para-1 o perfil à organização ativa), a modelagem baseada em relacionamento com `Organization` facilita a transição para um modelo **SaaS Multi-tenant**:

1.  **Isolamento de Dados (Tenancy):** Filtros nativos podem ser aplicados às consultas garantindo que cada usuário logado enxergue apenas o `CompanyProfile` atrelado ao `organization_id` de seu usuário.
2.  **Planos e Limitações:** É possível estender a lógica para bloquear recursos (ex: limite de orçamentos gerados, número de usuários e upload de logos em alta resolução) com base nas configurações da `Organization` ativa.
3.  **Upgrade de Domínios:** Mapear domínios específicos para cada organização a fim de servir portais operacionais e sites públicos personalizados para cada marmoraria assinante a partir da mesma base Django.
