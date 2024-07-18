from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticatedOrReadOnly
from account.models import User
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permissions(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or \
            (request.user.is_authenticated and (request.user.is_superuser or request.role == User.ADMIN))


class IsAuthenticatedOrOwnerOrReadOnly(IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly):
    pass
