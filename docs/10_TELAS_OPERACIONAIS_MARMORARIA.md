# Documentação das Telas Operacionais (EscolaSegura)

Esta documentação descreve o conjunto de telas comerciais (CRUDs) que foram implementadas no painel administrativo (`backoffice`) utilizando o template Skodash.

## Visão Geral

O módulo operacional é o core de vendas e serviços da escola, consistindo nos seguintes pilares:
- **Clientes**: Cadastro e manutenção de pessoas físicas e jurídicas.
- **Catálogo**: Cadastro de materiais (Chapas de Mármore, Granito, Quartzo, etc) e serviços de mão de obra e instalação (com unidade de medida m², ml, un, h).
- **Orçamentos**: Criação e gestão de propostas comerciais, incluindo cálculo automático de totais baseado nos itens de linha do catálogo. Suporte para múltiplos status (Rascunho, Em orçamento, Enviado, Aprovado, Rejeitado, Cancelado) e tela de "Preview PDF" pronta para impressão ou envio por e-mail/WhatsApp.
- **Vistorias**: Registros de serviços e medições técnicas associadas a clientes e orçamentos, incluindo apontamentos de técnico responsável, locais e observações.

## Arquitetura das Views

As views foram estruturadas em `apps/backoffice/views.py` e utilizam as funções baseadas no Django (`FBV - Function Based Views`) com o decorador `@login_required` garantindo a segurança de acesso ao painel. 

Fluxo de Criação e Edição:
1. **Listagem (`/app/modulo/`)**: Exibe uma tabela com os registros mais recentes (ex: `clientes.html`).
2. **Criação (`/app/modulo/novo/`)**: Apresenta um formulário limpo para inserção de dados. O envio via método `POST` salva o registro e redireciona para a listagem (ex: `clientes_novo.html`).
3. **Edição e Detalhes (`/app/modulo/<id>/`)**: Recupera o registro pelo ID, permitindo atualização (ex: `clientes_detalhe.html`). No caso de Orçamentos, esta view também suporta a adição e remoção de `EstimateLine` (itens).

## Integração com Log e Auditoria

Todas as alterações (Criação, Atualização, Exclusão, Mudança de Status) são automaticamente registradas no `ActivityLog` via função auxiliar `log_activity`, garantindo a rastreabilidade (ex: `estimate_status_updated`, `estimate_item_added`).

## Seed de Dados

O script `seed_escola_segura_demo.py` preenche o banco com uma vasta quantidade de informações simuladas (pedras famosas, clientes com nomes realistas, dezenas de orçamentos e vistorias). Para rodá-lo:
```bash
python manage.py seed_escola_segura_demo
```

## Como Demonstrar Comercial

1. **Dashboard**: Mostre a visão geral (painel) com números de vendas, conversão, leads.
2. **Catálogo**: Acesse a aba Catálogo e mostre como é fácil criar um novo produto com sua precificação (m² ou ml).
3. **Clientes**: Entre em clientes para visualizar a tabela limpa e editar um cliente.
4. **Orçamentos**: 
   - Mostre a tabela principal;
   - Clique em "Novo Orçamento", crie uma estrutura básica;
   - Entre no detalhe do orçamento criado, adicione itens do catálogo (bancada, cuba, instalação) e mude a quantidade. Veja o subtotal calcular;
   - Clique em "Visualizar/Imprimir PDF" para abrir a janela `preview`, demonstrando o aspecto premium que a escola poderá enviar ao cliente final.
5. **Vistorias**: Na sequência de um orçamento aprovado, mostre a tela de vistoria onde o medidor preenche relatórios de medidas de obra.

---
**Próximos Passos Sugeridos:**
- Implementar Integração real de envio por WhatsApp/E-mail nos Orçamentos usando as APIs.
- Adicionar uploads múltiplos nas fotos das Vistorias.
