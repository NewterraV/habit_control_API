from rest_framework.permissions import BasePermission
from django.utils.translation import gettext_lazy as _


class IsOwnerPermissions(BasePermission):
    """Проверка на принадлежность объекта аутентифицированному пользователю"""
    message = {'error': _('Вы не являетесь владельцем')}

    def has_object_permission(self, request, view, obj):
        return bool(obj.owner == request.user)
