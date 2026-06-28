class RequestAuditMiddleware:
    """Middleware leve. Registros detalhados ficam a cargo dos use cases/services."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)
