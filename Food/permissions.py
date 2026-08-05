from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # GET,HEAD,OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user_name == request.user


class IsStaffOrReadOnly(permissions.BasePermission):
    """Allow anyone to browse the menu, but reserve catalog changes for staff."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated and request.user.is_staff)
        )
