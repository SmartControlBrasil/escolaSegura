# Orçamento Profissional (Módulo de Vendas)

O módulo de orçamentos (Estimates) foi significativamente melhorado para atuar não apenas como uma ferramenta interna de cálculo, mas como o principal instrumento de fechamento de vendas da EscolaSegura.

## Novas Funcionalidades Arquiteturais

1. **Cálculo Automático de Área (m²):**
   O modelo `EstimateLine` agora aceita medidas explícitas de `length` (comprimento) e `width` (largura).
   - Se esses valores são maiores que 0, o backend calcula a área exata automaticamente sobrescrevendo a quantidade.
   - Isso elimina erros manuais e permite apresentar detalhadamente na proposta ("2.5m x 0.6m = 1.50 m²").
   - A lógica reside no método `save()` do modelo, não dependendo do frontend para garantir a integridade dos dados.

2. **Detalhamento da Proposta (UI):**
   A tela de detalhes do orçamento foi bifurcada em duas abas semânticas:
   - **Dados Gerais:** Responsável por cliente, endereço da obra, ambiente, condições de pagamento e prazos.
   - **Itens e Valores:** Uma área rica que permite adicionar dinamicamente insumos e serviços, inserir descontos em linha e observar os subtotais e descontos globais sendo consolidados instantaneamente.

3. **Preview Comercial para Impressão:**
   A rota `/app/orcamentos/<id>/preview/` renderiza a Proposta Comercial em um layout otimizado, claro e minimalista:
   - Elimina o layout "engessado" do backoffice.
   - Introduz o cabeçalho oficial da empresa e os blocos de dados de cliente e obra.
   - Detalha a tabela de itens.
   - Fornece um espaço dedicado para **condições comerciais** e **assinatura de aceite**.
   - Integração com `window.print()` (inclusive ocultando elementos estéticos desnecessários da UI usando `@media print`).

## Status e Auditoria

Os orçamentos refletem estados claros:
- Rascunho (`draft`)
- Enviado (`sent`)
- Aprovado (`approved`)
- Recusado (`rejected`)
- Expirado (`expired`)

A mudança manual de status na barra de cabeçalho salva e registra imediatamente na tabela de auditoria (via `log_activity`), rastreando as etapas do funil de vendas por colaborador.

## População de Dados (Seed)
A rotina `seed_escola_segura_demo` forja itens que testam este fluxo ao extremo, gerando automaticamente chapas e serviços que usam as variáveis `length` e `width` e calculando o imposto e desconto adequadamente para a demonstração comercial.
