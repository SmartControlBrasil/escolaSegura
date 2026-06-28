from django.utils import timezone

class FinancialStatusService:
    @staticmethod
    def mark_overdue(queryset):
        today = timezone.localdate()
        return queryset.filter(status='pending', due_date__lt=today).update(status='overdue')
