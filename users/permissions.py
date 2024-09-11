from rest_framework import permissions
from .models import User
from rest_framework.views import View


class IsSuperuser(permissions.BasePermission):
    def has_permission(self, request, view: View):
        return request.user.is_authenticated and request.user.is_superuser


class IsAccountOwner(permissions.BasePermission):
    def has_object_permission(self, request, view: View, obj: User) -> bool:
        return request.user.is_authenticated and obj == request.user
