"""
buscar_leads.py
===============
Management command do Django para captura automatizada de prospects pelo Atlas.

Uso:
    python manage.py buscar_leads
    python manage.py buscar_leads --fonte google_maps --cidade "São Paulo" --estado SP
    python manage.py buscar_leads --dry-run          # simula sem gravar no banco

Arquitetura:
    Este comando é o "gatilho" do robô Atlas. Ele orquestra a pipeline de
    captura em três etapas:

        1. COLETA   → ChaveiroDeColeta.coletar()
                      Chama a fonte de dados configurada (simulação, Google Maps,
                      scraper, API de terceiros, IA generativa, etc.) e retorna uma
                      lista de dicionários com os dados brutos dos prospects.

        2. QUALIFICAÇÃO → ChaveiroDeColeta.qualificar()
                      Aplica regras de negócio para calcular o score e decidir se
                      o prospect vai direto para 'review' ou é descartado.

        3. PERSISTÊNCIA → Grava no banco via AtlasProspect.objects.get_or_create()
                      usando company_name como chave de deduplicação.

Para integrar uma fonte real (Google Maps, OpenAI, scraper):
    Implemente a função `_coletar_<fonte>()` correspondente e registre-a
    em FONTES_DISPONIVEIS. O núcleo do comando não precisa mudar.
"""

import logging
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from apps.agents.infrastructure.models import AgentProfile, AtlasProspect

logger = logging.getLogger(__name__)

# ── Mapa de fontes disponíveis ────────────────────────────────────────────────
# Chave: slug usado no argumento --fonte
# Valor: callable que recebe (cidade, estado, limite) e retorna list[dict]
# Para adicionar uma nova fonte: implemente a função e registre aqui.
FONTES_DISPONIVEIS: dict[str, callable] = {}


# ─────────────────────────────────────────────────────────────────────────────
# FONTE: Simulação local (padrão quando nenhuma fonte real está configurada)
# Substitua esta função por uma integração real quando estiver pronto.
# ─────────────────────────────────────────────────────────────────────────────
def _coletar_simulacao(cidade: str, estado: str, limite: int) -> list[dict]:
    """
    Gera prospects fictícios para desenvolvimento e demonstração.

    Retorna uma lista de dicts compatíveis com os campos do AtlasProspect.
    Cada item representa um lead cru, antes da qualificação.

    SUBSTITUA esta função por:
      - requests + BeautifulSoup para scraping de portais (ex: GabaritoMaps)
      - googlemaps.Client para Google Places API
      - openai.ChatCompletion para extração via IA
      - seu próprio crawler assíncrono (Scrapy, Playwright etc.)
    """
    agora = datetime.now().strftime('%Y%m%d%H%M')
    leads_brutos = [
        {
            'company_name': f'Construtora Alpha {agora}',
            'website':       'https://construtoraalpha.com.br',
            'contact_name':  'Ricardo Almeida',
            'contact_email': f'contato+{agora}@construtoraalpha.com.br',
            'phone':         '(11) 91234-5678',
            'city':          cidade,
            'state':         estado,
            'source':        'simulacao',
            'evidence':      {
                'fonte': 'simulacao',
                'capturado_em': timezone.now().isoformat(),
                'palavras_chave': ['mármore', 'granito', 'acabamento'],
            },
            'notes': 'Lead gerado em modo simulação. Substituir por dado real.',
        },
        {
            'company_name': f'Arquitetura & Design Beta {agora}',
            'website':       'https://designbeta.com.br',
            'contact_name':  'Larissa Fontes',
            'contact_email': f'larissa+{agora}@designbeta.com.br',
            'phone':         '(11) 99876-5432',
            'city':          cidade,
            'state':         estado,
            'source':        'simulacao',
            'evidence':      {
                'fonte': 'simulacao',
                'capturado_em': timezone.now().isoformat(),
                'palavras_chave': ['interiores', 'piso', 'revestimento'],
            },
            'notes': 'Lead gerado em modo simulação. Substituir por dado real.',
        },
        {
            'company_name': f'Empreendimentos Gamma {agora}',
            'website':       'https://empreendimentosgamma.com.br',
            'contact_name':  'Paulo Souza',
            'contact_email': f'paulo+{agora}@empreendimentosgamma.com.br',
            'phone':         '(11) 97654-3210',
            'city':          cidade,
            'state':         estado,
            'source':        'simulacao',
            'evidence':      {
                'fonte': 'simulacao',
                'capturado_em': timezone.now().isoformat(),
                'palavras_chave': ['obra', 'incorporadora', 'apartamento'],
            },
            'notes': 'Lead gerado em modo simulação. Substituir por dado real.',
        },
    ]
    return leads_brutos[:limite]


# Registra a simulação como fonte padrão
FONTES_DISPONIVEIS['simulacao'] = _coletar_simulacao


# ─────────────────────────────────────────────────────────────────────────────
# REGRAS DE QUALIFICAÇÃO
# Aplique aqui a lógica de score e filtro antes de persistir.
# ─────────────────────────────────────────────────────────────────────────────
def _qualificar(lead_bruto: dict) -> tuple[int, bool]:
    """
    Calcula o score do lead e decide se ele deve ser persistido.

    Retorna:
        (score: int, deve_persistir: bool)

    Regras atuais (adapte conforme o negócio):
        +40  → tem e-mail de contato
        +30  → tem website
        +20  → tem nome do contato
        +10  → tem telefone
        ──────────────────────
        < 40 → descartado automaticamente (sem e-mail nem site = sem como contatar)
    """
    score = 0

    if lead_bruto.get('contact_email'):
        score += 40
    if lead_bruto.get('website'):
        score += 30
    if lead_bruto.get('contact_name'):
        score += 20
    if lead_bruto.get('phone'):
        score += 10

    deve_persistir = score >= 40  # exige pelo menos e-mail de contato
    return score, deve_persistir


# ─────────────────────────────────────────────────────────────────────────────
# COMANDO PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────
class Command(BaseCommand):
    help = (
        'Robô Atlas: captura prospects na web e os alimenta no banco de dados '
        'com status "review" para aprovação humana no painel /app/atlas/.'
    )

    # ── Argumentos CLI ────────────────────────────────────────────────────────
    def add_arguments(self, parser):
        parser.add_argument(
            '--fonte',
            type=str,
            default='simulacao',
            choices=list(FONTES_DISPONIVEIS.keys()),
            help=(
                'Fonte de dados a ser usada na captura. '
                f'Disponíveis: {", ".join(FONTES_DISPONIVEIS.keys())}. '
                'Padrão: simulacao.'
            ),
        )
        parser.add_argument(
            '--cidade',
            type=str,
            default='São Paulo',
            help='Cidade-alvo da busca de prospects. Padrão: São Paulo.',
        )
        parser.add_argument(
            '--estado',
            type=str,
            default='SP',
            help='UF do estado-alvo (2 letras). Padrão: SP.',
        )
        parser.add_argument(
            '--limite',
            type=int,
            default=10,
            help='Número máximo de prospects a capturar por execução. Padrão: 10.',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            default=False,
            help=(
                'Executa toda a pipeline (coleta + qualificação) mas NÃO '
                'grava nada no banco. Útil para testar a integração antes de '
                'colocar em produção.'
            ),
        )

    # ── Ponto de entrada ──────────────────────────────────────────────────────
    def handle(self, *args, **options):
        fonte_slug  = options['fonte']
        cidade      = options['cidade'].strip()
        estado      = options['estado'].upper().strip()[:2]
        limite      = max(1, min(options['limite'], 100))  # cap em 100 por segurança
        dry_run     = options['dry_run']

        self.stdout.write(self.style.HTTP_INFO(
            f'\n🤖 Atlas — Iniciando captura de leads'
        ))
        self.stdout.write(f'   Fonte   : {fonte_slug}')
        self.stdout.write(f'   Cidade  : {cidade}/{estado}')
        self.stdout.write(f'   Limite  : {limite} prospects')
        self.stdout.write(f'   Dry-run : {"SIM (nada será gravado)" if dry_run else "NÃO"}')
        self.stdout.write('─' * 54)

        # Valida que o AgentProfile do Atlas existe no banco
        # (criado pelo seed_base; necessário para rastreabilidade futura)
        atlas_agent = AgentProfile.objects.filter(kind='atlas', is_active=True).first()
        if not atlas_agent:
            raise CommandError(
                'AgentProfile do Atlas não encontrado. '
                'Execute "python manage.py seed_base" primeiro.'
            )

        # ── Etapa 1: Coleta ───────────────────────────────────────────────────
        self.stdout.write('\n📡 Etapa 1/3 — Coletando leads...')
        try:
            funcao_coleta = FONTES_DISPONIVEIS[fonte_slug]
            leads_brutos  = funcao_coleta(cidade, estado, limite)
        except Exception as exc:
            logger.exception('Falha na etapa de coleta do Atlas.')
            raise CommandError(f'Erro ao coletar leads da fonte "{fonte_slug}": {exc}') from exc

        self.stdout.write(self.style.SUCCESS(
            f'   ✓ {len(leads_brutos)} lead(s) coletado(s) da fonte "{fonte_slug}".'
        ))

        # ── Etapa 2: Qualificação ─────────────────────────────────────────────
        self.stdout.write('\n🔍 Etapa 2/3 — Qualificando leads...')
        leads_qualificados = []
        descartados        = 0

        for lead in leads_brutos:
            score, deve_persistir = _qualificar(lead)
            if deve_persistir:
                lead['score'] = score
                leads_qualificados.append(lead)
                self.stdout.write(
                    f'   ✓ Score {score:>3} — {lead.get("company_name", "?")} '
                    f'[{lead.get("city", "")}/{lead.get("state", "")}]'
                )
            else:
                descartados += 1
                self.stdout.write(self.style.WARNING(
                    f'   ✗ Score {score:>3} — {lead.get("company_name", "?")} descartado '
                    f'(score insuficiente)'
                ))

        self.stdout.write(
            f'\n   Qualificados : {len(leads_qualificados)} | '
            f'Descartados : {descartados}'
        )

        if not leads_qualificados:
            self.stdout.write(self.style.WARNING(
                '\n⚠️  Nenhum lead qualificado. Encerrando sem gravações.'
            ))
            return

        # ── Etapa 3: Persistência ─────────────────────────────────────────────
        self.stdout.write('\n💾 Etapa 3/3 — Persistindo no banco...')

        criados    = 0
        existentes = 0

        for lead in leads_qualificados:
            if dry_run:
                # Em dry-run, apenas loga sem gravar
                self.stdout.write(self.style.WARNING(
                    f'   [DRY-RUN] Não gravado: {lead.get("company_name")}'
                ))
                continue

            try:
                prospect, created = AtlasProspect.objects.get_or_create(
                    # Chave de deduplicação: empresa + cidade. Evita duplicatas
                    # em execuções consecutivas do mesmo robô.
                    company_name=lead['company_name'],
                    city=lead.get('city', ''),
                    defaults={
                        'website':       lead.get('website', ''),
                        'contact_name':  lead.get('contact_name', ''),
                        'contact_email': lead.get('contact_email', ''),
                        'phone':         lead.get('phone', ''),
                        'state':         lead.get('state', ''),
                        'source':        lead.get('source', fonte_slug),
                        'score':         lead.get('score', 0),
                        # Status 'review' → aparece automaticamente no painel Atlas
                        # aguardando decisão humana (aprovar/rejeitar)
                        'status':        AtlasProspect.Status.REVIEW,
                        'evidence':      lead.get('evidence', {}),
                        'notes':         lead.get('notes', ''),
                    },
                )

                if created:
                    criados += 1
                    self.stdout.write(self.style.SUCCESS(
                        f'   + CRIADO  : {prospect.company_name} '
                        f'(score: {prospect.score})'
                    ))
                    logger.info(
                        'Atlas: novo prospect criado — %s (%s/%s)',
                        prospect.company_name, prospect.city, prospect.state,
                    )
                else:
                    existentes += 1
                    self.stdout.write(
                        f'   ~ EXISTENTE: {prospect.company_name} '
                        f'(status atual: {prospect.get_status_display()})'
                    )

            except Exception as exc:
                logger.exception(
                    'Erro ao persistir prospect "%s".',
                    lead.get('company_name', '?'),
                )
                self.stdout.write(self.style.ERROR(
                    f'   ✗ ERRO ao gravar "{lead.get("company_name", "?")}": {exc}'
                ))

        # ── Resumo final ──────────────────────────────────────────────────────
        self.stdout.write('\n' + '─' * 54)
        if dry_run:
            self.stdout.write(self.style.WARNING(
                f'🏁 Dry-run concluído. '
                f'{len(leads_qualificados)} lead(s) qualificado(s) — '
                f'nada foi gravado no banco.'
            ))
        else:
            self.stdout.write(self.style.SUCCESS(
                f'🏁 Captura concluída!\n'
                f'   Criados    : {criados}\n'
                f'   Existentes : {existentes}\n'
                f'   Descartados: {descartados}\n\n'
                f'   Acesse /app/atlas/ para revisar os novos leads.'
            ))
