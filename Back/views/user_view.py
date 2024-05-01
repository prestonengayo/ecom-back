from django.contrib.auth.models import User
from Back.perm import IsAdmin
from rest_framework import viewsets
from Back.serializers.user_serializer import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        """
        Cette surcharge permet d'adapter le queryset en fonction de l'utilisateur.
        Si l'utilisateur n'est pas admin, il ne peut voir que son propre profil.
        """
        if self.request.user.profile.is_admin:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)
