from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrReadOnly(BasePermission):
    """Allows access (change/delete) only to author user."""
    message = ''

    def has_permission(self, request, view):
        self.message = 'Необходима авторизация.'

        return (
            request.method in SAFE_METHODS or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        self.message = 'Необходима авторство.'
        return request.method in SAFE_METHODS or request.user == obj.author


class IsAuthenticatedAndAdmin(BasePermission):
    """Authenticated administrator."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin()

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.is_admin()


class IsAuthenticatedAndModerator(BasePermission):
    """Authenticated moderator."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_moderator()

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.is_moderator()


class IsAuthenticatedAndSuperUser(BasePermission):
    """Authenticated superuser."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.is_superuser
