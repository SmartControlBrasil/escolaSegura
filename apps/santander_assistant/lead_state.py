"""
lead_state.py — Máquina de estados de coleta de lead
=====================================================

Princípio "um dado por turno":
    O visitante está conversando normalmente (DISCOVERY).  Quando demonstra
    intenção comercial explícita, o estado avança para COLLECT_NAME e inicia
    a coleta gradual:

        DISCOVERY  →  COLLECT_NAME  →  COLLECT_PHONE
              →  COLLECT_EMAIL  →  QUALIFIED

    Cada transição acontece somente depois que o serviço de orquestração
    valida e persiste o dado correspondente na sessão.

Regras de negócio:
    ● A coleta SÓ inicia se ``verificar_intencao_comercial()`` detectar
      palavras-chave de interesse real (orçamento, bancada, preço, etc.).
    ● Perguntas técnicas dentro do fluxo de coleta são respondidas primeiro;
      a coleta retoma na próxima mensagem (o estado NÃO regride).
    ● Um lead QUALIFIED não volta para coleta — a assistente continua
      respondendo normalmente, mas sem pedir dados novamente.
"""

from __future__ import annotations

import re
from typing import Optional

from django.db import models


# ─────────────────────────────────────────────────────────────────────────────
# Enum de estados
# ─────────────────────────────────────────────────────────────────────────────
class LeadState(models.TextChoices):
    """
    Estados possíveis da sessão na pipeline de captura de lead.

    A ordem importa: cada valor mapeia diretamente uma etapa do funil.
    """
    DISCOVERY     = 'discovery',      'Conversando'
    COLLECT_NAME  = 'collect_name',   'Coletando nome'
    COLLECT_PHONE = 'collect_phone',  'Coletando telefone'
    COLLECT_EMAIL = 'collect_email',  'Coletando e-mail'
    QUALIFIED     = 'qualified',      'Lead qualificado'


# ─────────────────────────────────────────────────────────────────────────────
# Transição de estados
# ─────────────────────────────────────────────────────────────────────────────
# Mapa de transições válidas: estado_atual → próximo_estado
_TRANSITIONS: dict[str, Optional[str]] = {
    LeadState.DISCOVERY:     LeadState.COLLECT_NAME,
    LeadState.COLLECT_NAME:  LeadState.COLLECT_PHONE,
    LeadState.COLLECT_PHONE: LeadState.COLLECT_EMAIL,
    LeadState.COLLECT_EMAIL: LeadState.QUALIFIED,
    LeadState.QUALIFIED:     None,  # estado terminal
}


def proximo_estado(estado_atual: str) -> Optional[str]:
    """
    Retorna o próximo estado válido a partir do estado atual.

    Retorna ``None`` se o estado atual for terminal (QUALIFIED)
    ou inválido.

    >>> proximo_estado('discovery')
    'collect_name'
    >>> proximo_estado('qualified')
    None
    """
    return _TRANSITIONS.get(estado_atual)


def is_coletando(estado: str) -> bool:
    """
    Retorna True se o estado indica que estamos no meio da coleta
    de dados de um lead (entre COLLECT_NAME e COLLECT_EMAIL inclusive).

    >>> is_coletando('collect_phone')
    True
    >>> is_coletando('discovery')
    False
    """
    return estado in (
        LeadState.COLLECT_NAME,
        LeadState.COLLECT_PHONE,
        LeadState.COLLECT_EMAIL,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Detecção de intenção comercial
# ─────────────────────────────────────────────────────────────────────────────

# Termos que indicam interesse real em serviço/produto da marmoraria.
# Organizados por categoria para facilitar manutenção e expansão.
_TERMOS_COMERCIAIS: list[str] = [
    # ── Ação comercial direta ────────────────────────────────────────────
    'orçamento', 'orcamento',
    'orcar', 'orçar',
    'cotação', 'cotacao',
    'cotar',
    'proposta',
    'preço', 'preco',
    'valor',
    'quanto custa', 'quanto fica', 'quanto sai',
    'me passa o preço', 'passa o valor',
    'preciso de um orçamento',
    'quero um orçamento',
    'fazer um orçamento',

    # ── Produtos de marmoraria ───────────────────────────────────────────
    'bancada', 'bancadas',
    'pia', 'pias',
    'lavatório', 'lavatorio',
    'ilha', 'ilhas',
    'soleira', 'soleiras',
    'peitoril', 'peitoris',
    'rodapé', 'rodape',
    'escada',
    'revestimento', 'revestimentos',
    'tampo', 'tampos',
    'mesa', 'mesas de pedra',
    'nicho', 'nichos',
    'banheira',
    'lareira',
    'piso de mármore', 'piso de granito',
    'churrasqueira',

    # ── Materiais específicos ────────────────────────────────────────────
    'mármore', 'marmore',
    'granito',
    'quartzo', 'quartzito',
    'silestone', 'dekton', 'caesarstone',
    'travertino',
    'porcelanato',
    'nanoglass',
    'limestone',

    # ── Serviços ─────────────────────────────────────────────────────────
    'medição', 'medicao',
    'instalação', 'instalacao',
    'instalar',
    'polimento',
    'restauração', 'restauracao',
    'impermeabilização', 'impermeabilizacao',
    'visita técnica', 'visita tecnica',

    # ── Contexto comercial ───────────────────────────────────────────────
    'obra',
    'reforma',
    'projeto',
    'apartamento',
    'casa',
    'cozinha',
    'banheiro', 'lavabo',
    'área gourmet', 'area gourmet',
    'varanda gourmet',
    'espaço gourmet', 'espaco gourmet',
]

# Regex compilada para performance: matcha qualquer termo como palavra inteira,
# ignorando acentos já que os termos estão duplicados com e sem acento.
_REGEX_COMERCIAL = re.compile(
    r'\b(?:' + '|'.join(re.escape(t) for t in _TERMOS_COMERCIAIS) + r')\b',
    re.IGNORECASE,
)


def verificar_intencao_comercial(mensagem_texto: str) -> bool:
    """
    Detecta se a mensagem do visitante contém intenção comercial explícita.

    A detecção é feita por matching de palavras-chave — simples,
    determinística e sem custo de API.  O serviço de orquestração só
    deve chamar esta função quando o estado atual for ``DISCOVERY``.

    Args:
        mensagem_texto: Texto cru da mensagem do visitante.

    Returns:
        True se pelo menos um termo comercial for encontrado.

    Exemplos:
        >>> verificar_intencao_comercial('Quero um orçamento de bancada')
        True
        >>> verificar_intencao_comercial('Bom dia, tudo bem?')
        False
        >>> verificar_intencao_comercial('Quanto custa uma pia de mármore?')
        True
        >>> verificar_intencao_comercial('Vocês fazem instalação?')
        True
    """
    if not mensagem_texto or not mensagem_texto.strip():
        return False
    return bool(_REGEX_COMERCIAL.search(mensagem_texto))


def termos_encontrados(mensagem_texto: str) -> list[str]:
    """
    Retorna a lista de termos comerciais encontrados na mensagem.

    Útil para logging e debugging do fluxo de detecção de intenção.

    Args:
        mensagem_texto: Texto cru da mensagem do visitante.

    Returns:
        Lista de strings com os termos detectados (pode ser vazia).

    Exemplos:
        >>> termos_encontrados('Preciso de uma bancada de granito para cozinha')
        ['bancada', 'granito', 'cozinha']
    """
    if not mensagem_texto or not mensagem_texto.strip():
        return []
    return [match.group() for match in _REGEX_COMERCIAL.finditer(mensagem_texto)]
