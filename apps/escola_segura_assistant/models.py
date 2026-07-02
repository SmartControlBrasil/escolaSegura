"""
models.py — Modelos de persistência da Assistente EscolaSegura
============================================================

Três modelos cobrem todo o ciclo de vida de uma conversa:

    EscolaSeguraChatSession
        Sessão de chat única vinculada ao visitante.  Armazena os dados
        do lead conforme são coletados (nome, telefone, e-mail) e o
        estado atual da máquina de estados (``current_state``).

    EscolaSeguraChatMessage
        Cada mensagem individual (user ou assistant) dentro de uma sessão.
        Garante auditoria completa e replay de contexto para o provider de IA.

    EscolaSeguraKnowledgeItem
        Item curado da base de conhecimento.  Respostas pré-editadas
        associadas a perguntas e tags para busca por keywords, sem
        necessidade de vector database no dia 1.

Todos herdam de ``TimeStampedModel`` (UUID pk + created_at + updated_at).
"""

from __future__ import annotations

from django.db import models

from apps.core.infrastructure.models import TimeStampedModel
from apps.escola_segura_assistant.lead_state import LeadState


# ─────────────────────────────────────────────────────────────────────────────
# Sessão de Chat
# ─────────────────────────────────────────────────────────────────────────────
class EscolaSeguraChatSession(TimeStampedModel):
    """
    Sessão de chat com um visitante do site.

    O ``session_key`` é gerado no frontend (UUID via ``crypto.randomUUID()``)
    e persistido no ``localStorage`` do navegador, permitindo retomar a
    mesma conversa em recarregamentos de página.

    O campo ``current_state`` reflete a posição do visitante na máquina
    de estados de coleta de lead (definida em ``lead_state.py``).
    """

    # Identificador público — gerado e mantido pelo frontend via localStorage
    session_key = models.CharField(
        max_length=64,
        unique=True,
        db_index=True,
        verbose_name='Chave da sessão',
        help_text='UUID gerado pelo navegador e persistido no localStorage.',
    )

    # ── Dados do lead (preenchidos progressivamente) ─────────────────────────
    client_name = models.CharField(
        max_length=160,
        blank=True,
        verbose_name='Nome do cliente',
    )
    client_phone = models.CharField(
        max_length=40,
        blank=True,
        verbose_name='Telefone / WhatsApp',
    )
    client_email = models.EmailField(
        blank=True,
        verbose_name='E-mail',
    )
    client_company = models.CharField(
        max_length=180,
        blank=True,
        verbose_name='Empresa / Escritório',
        help_text='Preenchido se o visitante for de construtora, escritório ou loja.',
    )
    client_city = models.CharField(
        max_length=120,
        blank=True,
        verbose_name='Cidade',
    )

    # ── Máquina de estados ───────────────────────────────────────────────────
    current_state = models.CharField(
        max_length=30,
        choices=LeadState.choices,
        default=LeadState.DISCOVERY,
        db_index=True,
        verbose_name='Estado atual do lead',
        help_text='Posição atual na máquina de estados de coleta.',
    )

    # ── Metadados ────────────────────────────────────────────────────────────
    source_page = models.CharField(
        max_length=500,
        blank=True,
        verbose_name='Página de origem',
        help_text='URL da página em que o visitante abriu o chat.',
    )
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name='Sessão ativa',
    )
    qualified_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Qualificado em',
        help_text='Data/hora em que o lead foi considerado qualificado.',
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Sessão de Chat'
        verbose_name_plural = 'Sessões de Chat'

    def __str__(self) -> str:
        nome = self.client_name or 'Visitante anônimo'
        return f'{nome} — {self.get_current_state_display()} ({self.session_key[:8]}…)'

    @property
    def is_qualified(self) -> bool:
        """Retorna True se o lead já completou toda a coleta de dados."""
        return self.current_state == LeadState.QUALIFIED


# ─────────────────────────────────────────────────────────────────────────────
# Mensagens do Chat
# ─────────────────────────────────────────────────────────────────────────────
class EscolaSeguraChatMessage(TimeStampedModel):
    """
    Mensagem individual dentro de uma sessão.

    O campo ``role`` segue a convenção padrão de LLMs (user / assistant / system)
    para facilitar a montagem do array de contexto ao chamar a API de IA.
    """

    class Role(models.TextChoices):
        USER = 'user', 'Visitante'
        ASSISTANT = 'assistant', 'Assistente'
        SYSTEM = 'system', 'Sistema'

    session = models.ForeignKey(
        EscolaSeguraChatSession,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='Sessão',
    )
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        verbose_name='Papel',
    )
    content = models.TextField(
        verbose_name='Conteúdo',
    )

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Mensagem'
        verbose_name_plural = 'Mensagens'

    def __str__(self) -> str:
        trecho = self.content[:60] + ('…' if len(self.content) > 60 else '')
        return f'[{self.get_role_display()}] {trecho}'


# ─────────────────────────────────────────────────────────────────────────────
# Base de Conhecimento (busca por keywords)
# ─────────────────────────────────────────────────────────────────────────────
class EscolaSeguraKnowledgeItem(TimeStampedModel):
    """
    Item curado de conhecimento para respostas rápidas.

    Cada registro mapeia uma pergunta frequente (ou variações via ``tags``)
    a uma resposta pré-editada.  A busca é feita por keywords nas tags —
    sem depender de embeddings ou vector DB.

    Exemplo:
        pergunta : "Qual a diferença entre mármore e granito?"
        resposta : "O mármore é uma rocha metamórfica, mais porosa..."
        tags     : "mármore, granito, diferença, comparação"
        categoria: "materiais"
    """

    class Category(models.TextChoices):
        MATERIAIS = 'materiais', 'Materiais (Mármore, Granito, Quartzo)'
        SERVICOS = 'servicos', 'Serviços (Instalação, Polimento, Medição)'
        PRODUTOS = 'produtos', 'Produtos (Bancada, Pia, Soleira, Ilha)'
        EMPRESA = 'empresa', 'Empresa (Horário, Localização, Garantia)'
        PROCESSO = 'processo', 'Processo (Prazos, Pagamento, Entrega)'
        CUIDADOS = 'cuidados', 'Cuidados e Manutenção'
        OUTROS = 'outros', 'Outros'

    pergunta = models.CharField(
        max_length=300,
        verbose_name='Pergunta / Título',
        help_text='A pergunta como o cliente faria (forma natural).',
    )
    resposta = models.TextField(
        verbose_name='Resposta',
        help_text='Resposta curada e aprovada pela equipe.',
    )
    tags = models.CharField(
        max_length=500,
        blank=True,
        verbose_name='Tags / Palavras-chave',
        help_text='Termos separados por vírgula usados na busca por keywords.',
    )
    categoria = models.CharField(
        max_length=30,
        choices=Category.choices,
        default=Category.OUTROS,
        verbose_name='Categoria',
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Ativo',
    )

    class Meta:
        ordering = ['categoria', 'pergunta']
        verbose_name = 'Item de Conhecimento'
        verbose_name_plural = 'Itens de Conhecimento'

    def __str__(self) -> str:
        return f'[{self.get_categoria_display()}] {self.pergunta[:80]}'
