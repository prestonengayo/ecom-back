from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Ajoutez des champs personnalisés
        token['user_id'] = user.id
        token['is_staff'] = user.is_staff
        token['is_admin'] = user.profile.is_admin
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # Ajout d'autres données personnalisées dans le token
        data.update({
            'user_id': self.user.id,
            'is_admin': self.user.profile.is_admin,
            'is_staff': self.user.is_staff
        })
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
