from apps.core.infrastructure.models import ActivityLog

class AuditService:
    @staticmethod
    def record(action: str, actor=None, organization=None, **metadata):
        return ActivityLog.objects.create(
            actor=actor if getattr(actor, 'is_authenticated', False) else None,
            organization=organization,
            action=action,
            metadata=metadata,
        )
