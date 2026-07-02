# Geração de PDFs e Relatórios de Entrega

Para transformar o painel comercial da EscolaSegura em uma verdadeira suíte de gestão de ponta a ponta, implementamos a geração nativa de relatórios PDF. Isso elimina a dependência de plataformas externas para gerar orçamentos e termos de aceite de obra.

## Biblioteca Utilizada
**WeasyPrint (v63.1+)**
- **Por que WeasyPrint?** É a biblioteca Python nativa mais avançada para renderização HTML->PDF. Ela interpreta CSS moderno nativamente (incluindo Flexbox e Grid) sem depender do obsoleto wkhtmltopdf.
- **Integração Django**: Usamos a função `render_to_string` nativa do Django para renderizar os templates HTML em memória, os quais o WeasyPrint compila em um PDF e devolve via `HttpResponse(content_type='application/pdf')`.

## Rotas de PDF Criadas

1. **PDF de Orçamento (`/app/orcamentos/<id>/pdf/`)**
   - Transforma a visualização `orcamentos_preview.html` em um arquivo físico A4.
   - Ideal para envio limpo por e-mail, sem interface de painel embutida.

2. **PDF de Entrega de Obra (`/app/entregas/<id>/pdf/`)**
   - Rota nova para gerar um termo oficial.
   - Apresenta cabeçalho da Escola, identificação do cliente e as métricas do checklist de entrega.
   - Fornece duas áreas de assinatura físicas ("Responsável Técnico" e "Cliente/Recebedor").

## Evolução do Modelo de Entregas (`ProjectDelivery`)
Para refletir um termo de entrega válido juridicamente/comercialmente, o modelo de banco de dados foi expandido para suportar micro-flags:
- `chk_parts_installed`: "Todas as peças instaladas?"
- `chk_finish_checked`: "Acabamento conferido?"
- `chk_cleaning_done`: "Limpeza feita?"
- `chk_customer_oriented`: "Cliente orientado?"

Na tela `/app/entregas/<id>/`, estes campos são botões "switches" dinâmicos e intuitivos que compõem a métrica do relatório em PDF.

## Limitações Atuais e Próximos Passos
- **Limitação (Fotos)**: Atualmente, os relatórios possuem apenas mocks (simulações) de imagens.
- **Limitação (Assinatura)**: A assinatura é "física" (linha tracejada para o PDF impresso).
- **Próximos Passos (Upload)**: Habilitar upload real pelo técnico via celular no ato da entrega, injetando os bytes (ou URL S3) das imagens diretamente no template HTML WeasyPrint.
- **Próximos Passos (Assinatura Digital)**: Implementar uma tela de "SignPad" em JS no mobile do técnico que salva a assinatura em Base64 e injeta no PDF gerado.
- **Próximos Passos (WhatsApp)**: Integrar Twilio ou similar para disparar o PDF imediatamente no celular do cliente via botão "Enviar ao Cliente".
