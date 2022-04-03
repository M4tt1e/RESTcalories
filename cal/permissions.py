from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Custom permission that only allows owners to edit own objects
    """
    def has_object_permission(self, request, view, obj):
        return obj.usr == request.user


class IsUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.username == request.user


