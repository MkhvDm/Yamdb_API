from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsModerator(BasePermission):
    """Allows access only for moderators."""
    def has_permission(self, request, view):
        return request.user.role == 'moderator'


class IsAdmin(BasePermission):
    """Allows access only for admins."""
    def has_permission(self, request, view):
        return request.user.role == 'admin'


class IsAuthor(BasePermission):
    """Allows access only for author."""
    def has_object_permission(self, request, view, obj):
        return request.user == obj.author


class ReadOnly(BasePermission):
    """Allows access for reading."""
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
