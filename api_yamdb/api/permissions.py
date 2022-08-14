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


class IsAdminOrReadOnly(BasePermission):
    """Проверка на роль админа или доступ только на чтение."""
    message = ''
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.role == 'admin'
        return False
