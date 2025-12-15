# api/permissions.py
from rest_framework.permissions import BasePermission

class EsOperativo(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and getattr(request.user, "rol", None)
            and request.user.rol.nombre.lower() == "operador"
        )

class EsSupervisor(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and getattr(request.user, "rol", None)
            and request.user.rol.nombre.lower() == "supervisor"
        )



