from rest_framework.permissions import BasePermission


class RecordPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated or not user.role:
            return False

        role = user.role.name

        if role == 'admin':
            return True

        if role == 'analyst':
            return request.method in ['GET']

        return False