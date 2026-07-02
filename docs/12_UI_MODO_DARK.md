# Modo Dark - Painel Skodash (EscolaSegura)

O template Skodash, utilizado no painel comercial administrativo (`/app/`), possui suporte nativo para múltiplas variações de tema, incluindo Dark, Light, Semi-Dark e Minimal.

## Implementação

Para garantir uma experiência de usuário de nível profissional, o suporte a temas foi aprimorado com **persistência via `localStorage`**. Isso significa que a preferência do usuário (modo escuro ou claro) é salva diretamente no navegador e mantida entre as navegações e recarregamentos da página, sem piscar a tela com conteúdo sem estilo (evitando o efeito *FOUC - Flash of Unstyled Content*).

### Como funciona

1. **Persistência (`localStorage`):** 
   As seleções feitas no painel lateral de temas do Skodash capturam o clique nos botões de rádio (`#DarkTheme`, `#LightTheme`, etc.) e salvam o valor na chave `skodash-theme` no `localStorage`.

2. **Prevenção de FOUC:** 
   No `head` do `base.html` (e também no `login.html`), um script síncrono é injetado imediatamente. Ele lê a chave `skodash-theme` e altera a classe do elemento `<html>` antes mesmo de o navegador processar o corpo da página, garantindo que o carregamento aconteça com as cores e contraste corretos.

3. **Isolamento de Segurança e Técnico:** 
   O painel de administração base do Django (`/admin/`), utilizado apenas por mantenedores técnicos, continua rodando de forma isolada, não herdando o CSS ou a política de temas do Skodash, mantendo a estabilidade padrão.

## Arquivos Alterados

- `templates/backoffice/base.html`: Inserido o script de aplicação síncrona do tema no `<head>` e o script de escuta do `localStorage` no rodapé.
- `templates/backoffice/login.html`: Importados os estilos de temas nativos do Skodash (`dark-theme.css`, `light-theme.css`, `semi-dark.css`) e inserido o script de aplicação para que o tema selecionado também valha na tela de login.
