"""
views.py — Endpoint HTTP da Assistente Santander
=================================================

View fina: toda lógica de negócio fica em ``services.py``.
A view apenas:
    1. Valida o método e o payload JSON
    2. Aplica rate-limiting e length checks
    3. Delega ao SantanderAssistantService
    4. Serializa a resposta como JsonResponse
"""

from __future__ import annotations

import json
import logging

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from apps.santander_assistant.prompts import SANTANDER_GREETING
from apps.santander_assistant.services import SantanderAssistantService

logger = logging.getLogger(__name__)


@csrf_exempt
@require_POST
def chat_endpoint(request):
    """
    Endpoint público da Assistente Santander.

    Contrato:
        POST /assistant/chat/
        Content-Type: application/json

        Request:
            {
                "message":     "texto do visitante",
                "session_key": "uuid-do-localstorage"  (opcional)
                "source_page": "/pagina/atual"         (opcional)
            }

        Response (200):
            {
                "conversation_id": "uuid",
                "reply":           "resposta da assistente",
                "lead_detected":   false,
                "session_key":     "uuid",
                "current_state":   "discovery"
            }

        Response (400): { "error": "descrição do erro" }
        Response (503): { "error": "assistente desabilitada" }

    Segurança:
        - @csrf_exempt: necessário para widget público (sem cookie de sessão)
        - Limite de 2000 caracteres por mensagem (configurável via settings)
        - Validação de Content-Type
    """

    # ── Feature flag ──────────────────────────────────────────────────────
    if not getattr(settings, 'SANTANDER_ASSISTANT_ENABLED', True):
        return JsonResponse(
            {'error': 'Assistente temporariamente desabilitada.'},
            status=503,
        )

    # ── Validação do payload ──────────────────────────────────────────────
    content_type = request.content_type or ''
    if 'json' not in content_type:
        return JsonResponse(
            {'error': 'Content-Type deve ser application/json.'},
            status=400,
        )

    try:
        payload = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse(
            {'error': 'Payload JSON inválido.'},
            status=400,
        )

    message = payload.get('message', '').strip()
    session_key = payload.get('session_key', '').strip()
    source_page = payload.get('source_page', '').strip()

    if not message:
        return JsonResponse(
            {'error': 'O campo "message" é obrigatório.'},
            status=400,
        )

    max_length = getattr(settings, 'SANTANDER_CHAT_MAX_MESSAGE_LENGTH', 2000)
    if len(message) > max_length:
        return JsonResponse(
            {'error': f'Mensagem excede o limite de {max_length} caracteres.'},
            status=400,
        )

    # ── Processamento ─────────────────────────────────────────────────────
    try:
        service = SantanderAssistantService()
        result = service.process_message(
            session_key=session_key,
            user_message_text=message,
            source_page=source_page,
        )
    except Exception:
        logger.exception('Santander Assistant: erro ao processar mensagem.')
        return JsonResponse(
            {'error': 'Erro interno ao processar a mensagem. Tente novamente.'},
            status=500,
        )

    # ── Resposta ──────────────────────────────────────────────────────────
    return JsonResponse({
        'conversation_id': result['conversation_id'],
        'reply': result['reply'],
        'lead_detected': result['lead_detected'],
        'session_key': result['session_key'],
        'current_state': result['current_state'],
    })


def greeting_endpoint(request):
    """
    GET /assistant/greeting/

    Retorna a mensagem de boas-vindas da assistente.
    Usado pelo widget para exibir a primeira mensagem sem POST.
    """
    return JsonResponse({
        'greeting': SANTANDER_GREETING,
        'assistant_name': 'Santander',
        'enabled': getattr(settings, 'SANTANDER_ASSISTANT_ENABLED', True),
    })
