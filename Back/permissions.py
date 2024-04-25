from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permission personnalisée pour permettre l'accès en lecture à tous,
    et l'accès en écriture uniquement aux utilisateurs admin.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True  # Autoriser les requêtes GET, HEAD ou OPTIONS
        return request.user.is_staff  # Seul l'admin peut modifier les données
