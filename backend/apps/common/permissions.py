from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == "admin")

class IsApprovedMember(BasePermission):
    """Company users who have passed admin approval."""
    def has_permission(self, request, view):
        u = request.user
        return bool(u and u.is_authenticated and u.role == "member" and u.is_approved)

class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role == "admin":
            return True
        owner = getattr(obj, "user", None) or getattr(obj, "owner", None)
        return owner == request.user

class ReadOnlyOrApprovedMember(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        u = request.user
        return bool(u and u.is_authenticated and (u.role == "admin" or (u.role == "member" and u.is_approved)))
