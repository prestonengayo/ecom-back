from rest_framework import permissions

class IsAdminOrSelf(permissions.BasePermission):
    """
    Permission personnalisée pour permettre aux utilisateurs de voir leurs propres détails,
    ou aux administrateurs de voir/modifier tous les détails.
    """

    def has_permission(self, request, view):
        # Tout le monde peut voir la liste si c'est un admin
        if request.method == 'GET' and view.action == 'list':
            return request.user.is_staff
        return True

    def has_object_permission(self, request, view, obj):
        # L'utilisateur peut modifier ses propres informations ou si c'est un admin
        return obj == request.user or request.user.is_staff
