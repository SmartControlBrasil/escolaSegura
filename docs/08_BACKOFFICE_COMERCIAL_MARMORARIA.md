# Backoffice Comercial Demonstrável - Marmoraria360

Este documento descreve a estrutura do painel de controle (backoffice) da Marmoraria360 (Marmoraria Santander), as rotas disponíveis, o fluxo comercial simulado e as credenciais necessárias para demonstração.

## Objetivos Comerciais

O objetivo principal desta versão do painel é servir como um piloto comercial robusto, realista e de alto impacto visual. Ele foi desenhado para simular todos os principais fluxos de uma marmoraria no dia a dia, com inteligência artificial e prospecção ativa prontas para demonstração a potenciais clientes (proprietários de marmorarias).

## Rotas Mapeadas no Skodash

O painel é acessado através do prefixo `/app/` e possui as seguintes telas:

1.  **Dashboard (`/app/`)**: Centraliza os 8 indicadores comerciais solicitados:
    *   *Leads do mês* (conversão de visitantes do site em leads)
    *   *Orçamentos abertos* (aguardando envio/aprovação)
    *   *Orçamentos aprovados* (prontos para ordem de serviço e corte)
    *   *Obras em andamento* (status operacional)
    *   *Vistorias agendadas* (medições marcadas com o cliente)
    *   *Faturamento estimado* (baseado nos orçamentos aprovados)
    *   *Taxa de conversão* (indicador comercial)
    *   *Pendências operacionais* (métrica de acompanhamento de gargalos)
2.  **Clientes (`/app/clientes/`)**: Lista os clientes com nome, tipo (Pessoa Física/Jurídica), contato, cidade e status.
3.  **Catálogo (`/app/catalogo/`)**: Lista materiais (Mármore, Granito, Silestone, Quartzo, Porcelanato) e serviços cadastrados, com unidade e preço de venda.
4.  **Orçamentos (`/app/orcamentos/`)**: Tabela com histórico de orçamentos, números identificadores únicos, valores totais e status de aprovação.
5.  **Novo Orçamento (`/app/orcamentos/novo/`)**: Formulário interativo para criação de um novo orçamento rascunho.
6.  **Vistorias (`/app/vistorias/`)**: Lista relatórios de vistoria técnica e medição milimétrica a laser presencial.
7.  **Relatórios (`/app/relatorios/`)**: Métricas e relatórios financeiros consolidados por status de orçamentos.
8.  **Redes Sociais (`/app/redes-sociais/`)**: Sugestões automáticas de posts com legendas, hashtags e sugestão de canal de publicação (marketing de prospecção).
9.  **Growth Engine (`/app/growth/`)**: Funil comercial exibindo as oportunidades em qualificação, proposta, negociação e fechamento.
10. **Robô Atlas (`/app/atlas/`)**: Painel onde o Atlas identifica prospects, sugere oportunidades e prepara dados/minutas para revisão humana.
11. **Assistente Virtual Lívia (`/app/assistente/`)**: Conversas do chat público capturadas no site, com resumos gerados de intenção de compra.
12. **Configurações (`/app/configuracoes/`)**: Dados de cadastro oficiais da empresa (Marmoraria Santander).

## Dados de Demonstração (Seed)

Para carregar todos os dados demonstrativos no banco de dados, execute:

```bash
python manage.py seed_marmoraria_demo
```

Este comando criará:
- **Organização principal** (Marmoraria Santander)
- **Usuário administrador** (`admin` / `admin123`)
- **Clientes residenciais e construtoras** com endereços e contatos.
- **Tabelas de preços** reais de chapas (Carrara, Nero Marquina, Preto São Gabriel, etc.) e serviços.
- **Orçamentos com diferentes status** e itens relacionados.
- **Vistorias e medições técnicas** completas.
- **Prospects de arquitetos e construtoras** (Atlas) em revisão.
- **Histórico de conversas** no bot do site público.

## Próximos Passos
- Implementar as regras de domínio usando a arquitetura DDD para conversão de orçamento aprovado em ordem de produção.
- Conectar canais de chat reais (WhatsApp/Telegram) e disparo de e-mails via provedor configurável.
