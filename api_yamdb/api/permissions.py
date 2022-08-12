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
