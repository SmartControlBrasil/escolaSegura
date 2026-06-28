class PolicyGuardService:
    """Checklist inicial de LGPD e segurança. Evolui para agente autônomo depois."""
    @staticmethod
    def run_basic_check():
        from apps.policy_guard.infrastructure.models import DataProcessingRecord, PolicyCheckRun
        findings = []
        if not DataProcessingRecord.objects.filter(is_active=True).exists():
            findings.append({'severity': 'medium', 'message': 'Nenhum registro de tratamento de dados ativo cadastrado.'})
        score = max(0, 100 - (len(findings) * 20))
        return PolicyCheckRun.objects.create(name='basic-lgpd-security-check', status='done', findings=findings, score=score)
