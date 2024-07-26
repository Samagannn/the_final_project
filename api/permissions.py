from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticatedOrReadOnly
from account.models import User


class IsOwnerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or \
            (request.user.is_authenticated and request.user == obj.user) or \
            (request.user.is_authenticated and request.user.is_superuser)


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or \
            (request.user.is_authenticated and (request.user.is_superuser or request.role == User.ADMIN))


class IsAuthenticatedOrOwnerOrReadOnly(IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly):
    pass
