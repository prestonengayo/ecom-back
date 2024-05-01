from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """
    Permission personnalisée pour permettre à l'administrateur d'accéder à toutes les données,
    et à l'utilisateur d'accéder uniquement à ses propres données.
    """

    def has_permission(self, request, view):
        # Seul l'admin peut accéder à la liste des utilisateurs
        if view.action == 'list':
            return request.user.profile.is_admin
        return True

    def has_object_permission(self, request, view, obj):
        # L'admin ou l'utilisateur lui-même peut voir, modifier ou supprimer son propre profil
        return obj == request.user or request.user.profile.is_admin
