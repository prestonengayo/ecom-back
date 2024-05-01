from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permission personnalisée pour permettre l'accès en lecture à tous,
    et l'accès en écriture uniquement aux utilisateurs admin.
    """

    def has_permission(self, request, view):
        # Tout le monde peut lire (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        # Seuls les admins peuvent modifier ou supprimer
        return request.user and request.user.profile.is_admin

    def has_object_permission(self, request, view, obj):
        # L'accès en lecture est permis à tout le monde
        if request.method in permissions.SAFE_METHODS:
            return True
        # L'accès en écriture est seulement permis aux admins
        return request.user and request.user.profile.is_admin
