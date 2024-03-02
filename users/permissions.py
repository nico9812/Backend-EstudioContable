from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsContador(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='contador').exists()


class IsCliente(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='cliente').exists()
