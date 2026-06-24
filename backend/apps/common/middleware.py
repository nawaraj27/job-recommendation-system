class AuditLogMiddleware:
    """Logs mutating admin/api actions for audit trail."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        try:
            if request.method in ("POST", "PUT", "PATCH", "DELETE") and request.path.startswith("/api/"):
                from .models import AuditLog
                user = request.user if getattr(request, "user", None) and request.user.is_authenticated else None
                AuditLog.objects.create(
                    user=user, method=request.method, path=request.path[:255],
                    status_code=getattr(response, "status_code", None),
                    ip=request.META.get("REMOTE_ADDR"),
                )
        except Exception:
            pass
        return response
