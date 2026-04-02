from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False
    
        return user.role and user.role.name == "admin"
    
class IsAdminOrAnalyst(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated or not user.role:
            return False

        return user.role.name in ['admin', 'analyst']