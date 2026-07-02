"""
services.py — Serviço de orquestração da Assistente Santander
==============================================================

Camada central que implementa TODA a lógica de negócio do chat.
A view é fina e apenas serializa/desserializa — a inteligência está aqui.

Responsabilidades:
    1. Gerenciamento de sessão (get_or_create_session)
    2. Processamento de mensagens (process_message)
    3. Máquina de estados do lead (coleta e validação de dados)
    4. Busca na base de conhecimento (fallback/RAG manual)
    5. Integração com provider de IA (Gemini ou fallback determinístico)

Princípio Fallback-First:
    O sistema SEMPRE funciona sem API key.  O provider Gemini é opcional
    e só é chamado quando:
      - SANTANDER_AI_PROVIDER='gemini'
      - GEMINI_API_KEY está configurada
      - A mensagem não é tratada por regras bloqueantes (preço, emergência)
    Em qualquer falha do provider, o fallback determinístico responde.
"""

from __future__ import annotations

import logging
import re
import uuid
import requests
from typing import Optional

from django.conf import settings
from django.db.models import Q
from django.utils import timezone

from apps.santander_assistant.lead_state import (
    LeadState,
    is_coletando,
    proximo_estado,
    verificar_intencao_comercial,
)
from apps.santander_assistant.models import (
    SantanderChatMessage,
    SantanderChatSession,
    SantanderKnowledgeItem,
)
from apps.santander_assistant.prompts import (
    LEAD_COLLECT_PROMPTS,
    SANTANDER_GREETING,
    SANTANDER_SYSTEM_PROMPT,
)

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# Regex de validação para dados do lead
# ─────────────────────────────────────────────────────────────────────────────

# Nome: pelo menos duas palavras com no mínimo 2 caracteres cada
_REGEX_NOME = re.compile(r'^[A-Za-zÀ-ÿ]{2,}(?:\s+[A-Za-zÀ-ÿ]{2,})+$')

# Telefone brasileiro: (XX) 9XXXX-XXXX ou variações com/sem parênteses,
# espaços, hifens. Aceita 10-11 dígitos.
_REGEX_TELEFONE = re.compile(
    r'^\(?\d{2}\)?[\s.-]?\d{4,5}[\s.-]?\d{4}$'
)

# E-mail: validação básica (o Django EmailField cuida do resto no model)
_REGEX_EMAIL = re.compile(
    r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
)

# Termos que indicam emergência / risco de segurança
_TERMOS_EMERGENCIA = re.compile(
    r'\b(?:rachad|trisc|quebr|ca[ií][ru]|desab|despenc|solt[oa]|pend[ue]'
    r'|perigo|acident|emerg[eê]nci|sangue|machucar|ferimento)\w*\b',
    re.IGNORECASE,
)

# Termos que tentam extrair preço (guardrail anti-invenção)
_TERMOS_PRECO = re.compile(
    r'\b(?:quanto\s+custa|quanto\s+fica|quanto\s+sai|qual\s+(?:o\s+)?'
    r'(?:valor|preço|preco|custo)|preço\s+(?:do|da|por)|me\s+pass[ea]\s+'
    r'(?:o\s+)?(?:valor|preço|preco)|tabela\s+de\s+preço'
    r'|valor\s+(?:do|da|por)\s+m(?:²|2|etro))\b',
    re.IGNORECASE,
)

# ─────────────────────────────────────────────────────────────────────────────
# Respostas determinísticas (guardrails Python, não dependem de LLM)
# ─────────────────────────────────────────────────────────────────────────────

_RESPOSTA_PRECO = (
    'Os valores dependem do material escolhido, das medidas do projeto e do '
    'tipo de acabamento. Para um orçamento preciso, nossa equipe técnica '
    'precisa avaliar os detalhes do seu projeto. '
    'Posso coletar seus dados para que alguém entre em contato?'
)

_RESPOSTA_EMERGENCIA = (
    'Por segurança, afaste-se da área afetada imediatamente. '
    'Entre em contato direto com nossa equipe pelo telefone informado no site. '
    'Não tente reparar sozinho — peças de pedra são pesadas e podem causar acidentes.'
)

_RESPOSTA_FORA_ESCOPO = (
    'Minha especialidade é ajudar com projetos em mármore, granito e pedras '
    'decorativas. Posso ajudar com algo nessa área?'
)

_RESPOSTA_FALLBACK = (
    'Entendi sua mensagem! Se quiser saber mais sobre nossos materiais, '
    'serviços ou solicitar um orçamento, estou à disposição.'
)

_RESPOSTA_VALIDACAO_NOME = (
    'Desculpe, não consegui captar seu nome completo. '
    'Pode informar seu nome e sobrenome, por favor?'
)

_RESPOSTA_VALIDACAO_TELEFONE = (
    'Hmm, não consegui identificar o número. '
    'Pode digitar no formato (XX) XXXXX-XXXX?'
)

_RESPOSTA_VALIDACAO_EMAIL = (
    'Parece que o e-mail não está no formato correto. '
    'Pode verificar e digitar novamente? Exemplo: seunome@email.com'
)


# ─────────────────────────────────────────────────────────────────────────────
# Serviço principal
# ─────────────────────────────────────────────────────────────────────────────
class SantanderAssistantService:
    """
    Serviço de orquestração da Assistente Santander.

    Uso típico (na view):
        service = SantanderAssistantService()
        result  = service.process_message(session_key, texto)
        # result = { 'reply': str, 'lead_detected': bool, ... }
    """

    # ── Sessão ────────────────────────────────────────────────────────────────

    @staticmethod
    def get_or_create_session(
        session_key: str,
        source_page: str = '',
    ) -> tuple[SantanderChatSession, bool]:
        """
        Retorna a sessão existente ou cria uma nova.

        Se o ``session_key`` recebido for vazio ou inválido, um novo UUID
        é gerado server-side e devolvido ao frontend na resposta JSON.

        Returns:
            (session, created)
        """
        if not session_key or len(session_key) > 64:
            session_key = str(uuid.uuid4())

        session, created = SantanderChatSession.objects.get_or_create(
            session_key=session_key,
            defaults={
                'source_page': source_page[:500] if source_page else '',
            },
        )

        if created:
            logger.info(
                'Santander Assistant: nova sessão criada — %s (page=%s)',
                session_key[:8], source_page[:80],
            )

        return session, created

    # ── Processamento principal ───────────────────────────────────────────────

    def process_message(
        self,
        session_key: str,
        user_message_text: str,
        source_page: str = '',
    ) -> dict:
        """
        Ponto de entrada principal do fluxo de conversa.

        Orquestra em ordem:
            1. Recupera/cria sessão
            2. Persiste mensagem do usuário
            3. Verifica guardrails bloqueantes (emergência, preço)
            4. Se em coleta → valida/persiste dado → avança estado
            5. Se em discovery → verifica intenção comercial
            6. Busca na base de conhecimento (fallback/RAG)
            7. Se nenhuma regra tratou → chama provider de IA
            8. Persiste resposta da assistente
            9. Retorna dict com a resposta e metadados

        Args:
            session_key:      UUID do localStorage do visitante.
            user_message_text: Texto da mensagem do visitante.
            source_page:      URL da página de origem.

        Returns:
            Dict com chaves: reply, conversation_id, session_key,
            lead_detected, current_state.
        """
        # 1. Sessão
        session, _ = self.get_or_create_session(session_key, source_page)

        # 2. Persiste mensagem do usuário
        SantanderChatMessage.objects.create(
            session=session,
            role=SantanderChatMessage.Role.USER,
            content=user_message_text,
        )

        # 3. Guardrails bloqueantes (Python-side, não LLM)
        reply = self._verificar_guardrails(user_message_text, session)
        lead_detected = False

        if reply is None:
            # 4. Máquina de estados do lead
            if is_coletando(session.current_state):
                reply = self._processar_coleta(session, user_message_text)

            elif session.current_state == LeadState.DISCOVERY:
                # 5. Verifica intenção comercial
                if verificar_intencao_comercial(user_message_text):
                    lead_detected = True
                    session.current_state = LeadState.COLLECT_NAME
                    session.save(update_fields=['current_state', 'updated_at'])
                    logger.info(
                        'Santander Assistant: intenção comercial detectada — sessão %s',
                        session.session_key[:8],
                    )

            # 6. Se ainda não temos resposta, tenta knowledge base + IA
            if reply is None:
                # Busca na base de conhecimento curada
                knowledge_reply = self._buscar_knowledge(user_message_text)

                if knowledge_reply:
                    reply = knowledge_reply
                else:
                    # 7. Provider de IA (Gemini ou fallback)
                    reply = self._gerar_resposta_ia(session, user_message_text)

                # Se detectou intenção comercial E a resposta veio de
                # knowledge/IA, anexa o prompt de coleta de nome
                if lead_detected and session.current_state == LeadState.COLLECT_NAME:
                    prompt_coleta = LEAD_COLLECT_PROMPTS.get('collect_name', '')
                    reply = f'{reply}\n\n{prompt_coleta}'

        # 8. Persiste resposta da assistente
        SantanderChatMessage.objects.create(
            session=session,
            role=SantanderChatMessage.Role.ASSISTANT,
            content=reply,
        )

        # 9. Retorna resposta
        return {
            'reply': reply,
            'conversation_id': str(session.pk),
            'session_key': session.session_key,
            'lead_detected': lead_detected,
            'current_state': session.current_state,
        }

    # ── Guardrails bloqueantes ────────────────────────────────────────────────

    @staticmethod
    def _verificar_guardrails(
        mensagem: str,
        session: SantanderChatSession,
    ) -> Optional[str]:
        """
        Verifica regras bloqueantes que NÃO devem passar para o LLM.

        Ordem de prioridade:
            1. Emergência → resposta fixa de segurança
            2. Pergunta de preço → resposta anti-invenção
               (se em discovery, também inicia coleta)

        Retorna a resposta fixa ou None se nenhum guardrail disparou.
        """
        # Emergência: prioridade máxima
        if _TERMOS_EMERGENCIA.search(mensagem):
            logger.warning(
                'Santander Assistant: EMERGÊNCIA detectada — sessão %s',
                session.session_key[:8],
            )
            return _RESPOSTA_EMERGENCIA

        # Preço: impede que o LLM invente valores
        if _TERMOS_PRECO.search(mensagem):
            # Se ainda está em discovery, aproveita para iniciar coleta
            if session.current_state == LeadState.DISCOVERY:
                session.current_state = LeadState.COLLECT_NAME
                session.save(update_fields=['current_state', 'updated_at'])
                prompt_coleta = LEAD_COLLECT_PROMPTS.get('collect_name', '')
                return f'{_RESPOSTA_PRECO}\n\n{prompt_coleta}'
            return _RESPOSTA_PRECO

        return None

    # ── Processamento da coleta de lead ───────────────────────────────────────

    def _processar_coleta(
        self,
        session: SantanderChatSession,
        mensagem: str,
    ) -> str:
        """
        Processa a mensagem no contexto da coleta de dados do lead.

        Valida o dado correspondente ao estado atual e, se válido:
            1. Persiste no campo da sessão
            2. Avança para o próximo estado
            3. Retorna o prompt de coleta do próximo campo

        Se inválido, retorna mensagem de re-solicitação (sem avançar).
        """
        estado = session.current_state
        texto = mensagem.strip()

        # ── COLLECT_NAME ─────────────────────────────────────────────────
        if estado == LeadState.COLLECT_NAME:
            nome = self._validar_nome(texto)
            if nome:
                session.client_name = nome
                session.current_state = proximo_estado(estado)
                session.save(update_fields=[
                    'client_name', 'current_state', 'updated_at',
                ])
                prompt = LEAD_COLLECT_PROMPTS.get('collect_phone', '')
                return prompt.format(client_name=nome)
            return _RESPOSTA_VALIDACAO_NOME

        # ── COLLECT_PHONE ────────────────────────────────────────────────
        if estado == LeadState.COLLECT_PHONE:
            telefone = self._validar_telefone(texto)
            if telefone:
                session.client_phone = telefone
                session.current_state = proximo_estado(estado)
                session.save(update_fields=[
                    'client_phone', 'current_state', 'updated_at',
                ])
                return LEAD_COLLECT_PROMPTS.get('collect_email', '')
            return _RESPOSTA_VALIDACAO_TELEFONE

        # ── COLLECT_EMAIL ────────────────────────────────────────────────
        if estado == LeadState.COLLECT_EMAIL:
            email = self._validar_email(texto)
            if email:
                session.client_email = email
                session.current_state = LeadState.QUALIFIED
                session.qualified_at = timezone.now()
                session.save(update_fields=[
                    'client_email', 'current_state',
                    'qualified_at', 'updated_at',
                ])
                logger.info(
                    'Santander Assistant: LEAD QUALIFICADO — %s (%s) — sessão %s',
                    session.client_name, session.client_email,
                    session.session_key[:8],
                )
                
                # Dispara o webhook em tempo real
                self._disparar_webhook_lead(session)
                
                prompt = LEAD_COLLECT_PROMPTS.get('qualified', '')
                return prompt.format(client_name=session.client_name)
            return _RESPOSTA_VALIDACAO_EMAIL

        # Estado desconhecido ou terminal — não deveria chegar aqui
        return _RESPOSTA_FALLBACK

    # ── Validadores ───────────────────────────────────────────────────────────

    @staticmethod
    def _validar_nome(texto: str) -> Optional[str]:
        """
        Valida e normaliza o nome do visitante.

        Aceita: "João Silva", "Maria da Conceição"
        Rejeita: "ok", "sim", "tudo bem", strings curtas demais
        """
        texto = texto.strip()
        # Rejeita respostas genéricas curtas
        if len(texto) < 4:
            return None
        # Rejeita termos comuns que não são nomes
        termos_invalidos = {
            'sim', 'não', 'nao', 'ok', 'tudo bem', 'claro',
            'pode ser', 'bom dia', 'boa tarde', 'boa noite',
            'obrigado', 'obrigada', 'valeu',
        }
        if texto.lower() in termos_invalidos:
            return None
        # Aceita nome + sobrenome OU nome simples com >= 3 letras
        if _REGEX_NOME.match(texto):
            return texto.title()
        # Se não tem espaço mas é um nome razoável (>= 3 letras, só alfa)
        if len(texto) >= 3 and texto.replace(' ', '').isalpha():
            return texto.title()
        return None

    @staticmethod
    def _validar_telefone(texto: str) -> Optional[str]:
        """
        Valida e normaliza telefone brasileiro.

        Aceita: (11) 91234-5678, 11912345678, 11 91234 5678
        Rejeita: strings sem dígitos suficientes
        """
        # Extrai somente dígitos
        digitos = re.sub(r'\D', '', texto)
        if len(digitos) < 10 or len(digitos) > 11:
            return None
        # Formata no padrão brasileiro
        if len(digitos) == 11:
            return f'({digitos[:2]}) {digitos[2:7]}-{digitos[7:]}'
        return f'({digitos[:2]}) {digitos[2:6]}-{digitos[6:]}'

    @staticmethod
    def _validar_email(texto: str) -> Optional[str]:
        """
        Valida e-mail básico.

        Rejeita: "sim", "ok", textos sem @
        """
        texto = texto.strip().lower()
        # Rejeita e-mails claramente fake
        if texto in ('sim@sim.com', 'nao@nao.com', 'teste@teste.com'):
            return None
        if _REGEX_EMAIL.match(texto):
            return texto
        return None

    # ── Busca na base de conhecimento ─────────────────────────────────────────

    @staticmethod
    def _buscar_knowledge(mensagem: str) -> Optional[str]:
        """
        Busca na base SantanderKnowledgeItem por matching de keywords.

        Estratégia:
            1. Tokeniza a mensagem em palavras (>= 3 chars)
            2. Para cada KnowledgeItem ativo, verifica quantas tags matcham
            3. Retorna a resposta do item com MAIS matches (mínimo 1)

        Returns:
            Texto da resposta curada ou None se nenhum item matchou.
        """
        # Tokeniza a mensagem em palavras significativas
        palavras = set(
            w.lower()
            for w in re.findall(r'[A-Za-zÀ-ÿ]+', mensagem)
            if len(w) >= 3
        )

        if not palavras:
            return None

        items = SantanderKnowledgeItem.objects.filter(is_active=True)
        melhor_item: Optional[SantanderKnowledgeItem] = None
        melhor_score = 0

        for item in items:
            tags = set(
                t.strip().lower()
                for t in item.tags.split(',')
                if t.strip()
            )
            # Conta interseção entre palavras da mensagem e tags do item
            score = len(palavras & tags)
            if score > melhor_score:
                melhor_score = score
                melhor_item = item

        if melhor_item and melhor_score >= 1:
            logger.debug(
                'Santander Assistant: knowledge match (score=%d) — "%s"',
                melhor_score, melhor_item.pergunta[:60],
            )
            return melhor_item.resposta

        return None

    # ── Provider de IA ────────────────────────────────────────────────────────

    def _gerar_resposta_ia(
        self,
        session: SantanderChatSession,
        mensagem: str,
    ) -> str:
        """
        Gera resposta usando provider de IA (Gemini) ou fallback.

        Fluxo:
            1. Se SANTANDER_AI_PROVIDER != 'gemini' → fallback
            2. Se GEMINI_API_KEY vazia → fallback
            3. Tenta Gemini com system prompt + histórico
            4. Em caso de exceção → fallback com log de erro
        """
        provider = getattr(settings, 'SANTANDER_AI_PROVIDER', 'fallback')
        api_key = getattr(settings, 'GEMINI_API_KEY', '')

        if provider != 'gemini' or not api_key:
            return self._resposta_fallback(mensagem, session)

        try:
            return self._chamar_gemini(session, mensagem, api_key)
        except Exception:
            logger.exception(
                'Santander Assistant: falha no Gemini — fallback ativado (sessão %s)',
                session.session_key[:8],
            )
            return self._resposta_fallback(mensagem, session)

    def _chamar_gemini(
        self,
        session: SantanderChatSession,
        mensagem: str,
        api_key: str,
    ) -> str:
        """
        Chama a API do Google Gemini com system prompt e histórico.

        O histórico é limitado às últimas 20 mensagens para manter o
        contexto gerenciável sem estourar o token budget.
        """
        import google.generativeai as genai

        genai.configure(api_key=api_key)

        model_name = getattr(settings, 'SANTANDER_AI_MODEL', 'gemini-2.0-flash')
        temperature = getattr(settings, 'SANTANDER_AI_TEMPERATURE', 0.4)
        max_tokens = getattr(settings, 'SANTANDER_AI_MAX_TOKENS', 500)

        model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=SANTANDER_SYSTEM_PROMPT,
            generation_config=genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
            ),
        )

        # Monta o histórico de conversa (últimas 20 mensagens)
        historico_msgs = session.messages.order_by('created_at')[:20]
        historico = []
        for msg in historico_msgs:
            role = 'user' if msg.role == 'user' else 'model'
            historico.append({'role': role, 'parts': [msg.content]})

        # Inicia o chat com o histórico existente (sem a mensagem atual,
        # que já foi persistida mas será enviada como send_message)
        # Remove a última mensagem do histórico pois é a mensagem atual
        # que será enviada via send_message
        if historico and historico[-1]['role'] == 'user':
            historico = historico[:-1]

        chat = model.start_chat(history=historico)
        response = chat.send_message(mensagem)

        reply = response.text.strip() if response.text else _RESPOSTA_FALLBACK

        logger.info(
            'Santander Assistant: Gemini respondeu — sessão %s (model=%s)',
            session.session_key[:8], model_name,
        )

        return reply

    @staticmethod
    def _resposta_fallback(mensagem: str, session: SantanderChatSession) -> str:
        """
        Fallback determinístico — responde sem API externa.

        Cobre os cenários mais comuns com respostas pré-definidas.
        É o modo padrão em desenvolvimento e o safety net em produção.
        """
        texto = mensagem.lower()

        # Saudações
        saudacoes = ('oi', 'olá', 'ola', 'bom dia', 'boa tarde', 'boa noite', 'hey', 'eae')
        if any(texto.startswith(s) or texto == s for s in saudacoes):
            return SANTANDER_GREETING

        # Materiais
        if any(m in texto for m in ('mármore', 'marmore', 'granito', 'quartzo', 'quartzito')):
            return (
                'Trabalhamos com uma ampla variedade de materiais: **mármore** nacional '
                'e importado, **granito**, **quartzito**, quartzo engineered (**Silestone**, '
                '**Dekton**), travertino e nanoglass. Cada material tem características '
                'diferentes de resistência, porosidade e estética. '
                'Quer saber mais sobre algum material específico?'
            )

        # Serviços
        if any(s in texto for s in ('instalação', 'instalacao', 'polimento', 'restauração', 'restauracao', 'impermeabilização')):
            return (
                'Oferecemos serviços completos: medição em obra, corte e acabamento de '
                'peças, instalação com equipe especializada, polimento, restauração e '
                'impermeabilização de superfícies. '
                'Qual serviço seria do seu interesse?'
            )

        # Produtos
        if any(p in texto for p in ('bancada', 'pia', 'lavatório', 'lavatorio', 'ilha', 'soleira')):
            return (
                'Produzimos peças sob medida: bancadas de cozinha, ilhas, pias, '
                'lavatórios, soleiras, peitoris e muito mais. Tudo com acabamento '
                'de alto padrão e instalação por nossa equipe. '
                'Qual peça você está buscando?'
            )

        # Processo / como funciona
        if any(p in texto for p in ('como funciona', 'processo', 'etapas', 'prazo', 'entrega')):
            return (
                'Nosso processo é simples: você solicita um orçamento, nossa equipe '
                'faz a visita técnica para medição, preparamos uma proposta detalhada, '
                'e após aprovação iniciamos a produção e instalação. '
                'O prazo varia conforme o projeto, mas trabalhamos com pontualidade.'
            )

        # Horário / endereço (sem inventar)
        if any(h in texto for h in ('horário', 'horario', 'endereço', 'endereco', 'localização', 'localizacao', 'onde fica')):
            return (
                'Para informações atualizadas sobre horário de funcionamento e '
                'endereço, consulte a página de contato no nosso site. '
                'Posso ajudar com algo sobre nossos materiais ou serviços?'
            )

        # Obrigado / despedida
        if any(d in texto for d in ('obrigado', 'obrigada', 'valeu', 'tchau', 'até mais', 'ate mais')):
            nome = session.client_name or 'você'
            return (
                f'Por nada, {nome}! Foi um prazer ajudar. '
                f'Se precisar de algo mais sobre mármores, granitos ou orçamentos, '
                f'é só me chamar. Até logo!'
            )

        # Fallback genérico
        return _RESPOSTA_FALLBACK

    def _disparar_webhook_lead(self, session: SantanderChatSession) -> None:
        """
        Dispara um webhook com os dados do lead qualificado.

        Lê a URL de destino das configurações de ambiente. Se vazia,
        o envio é silenciado com log informativo.
        """
        url = getattr(settings, 'SANTANDER_LEAD_WEBHOOK_URL', '')
        if not url:
            logger.info('Santander Assistant: Webhook de leads não configurado (SANTANDER_LEAD_WEBHOOK_URL vazio).')
            return

        payload = {
            'event': 'lead_qualified',
            'timestamp': timezone.now().isoformat(),
            'session_key': session.session_key,
            'data': {
                'name': session.client_name,
                'phone': session.client_phone,
                'email': session.client_email,
                'company': session.client_company,
                'city': session.client_city,
                'source_page': session.source_page,
                'qualified_at': session.qualified_at.isoformat() if session.qualified_at else None
            }
        }

        try:
            logger.info('Santander Assistant: Disparando webhook para %s', url)
            response = requests.post(url, json=payload, timeout=5)
            response.raise_for_status()
            logger.info('Santander Assistant: Webhook disparado com sucesso. Status: %s', response.status_code)
        except requests.exceptions.RequestException as exc:
            logger.error('Santander Assistant: Falha ao disparar webhook para %s. Erro: %s', url, exc)

