from django.contrib.auth.models import User
from rest_framework import serializers
from Back.models.user import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'address', 'email', 'phone', 'profile_image']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)  # Modifier ici pour permettre les mises à jour partielles

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'profile']
        extra_kwargs = {'password': {'write_only': True, 'required': False}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)  # Ceci est correct pour éviter KeyError lors du pop
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        
        # Gérer correctement l'absence de données de profil
        if profile_data is not None:  # Assurez-vous que profile_data n'est pas None avant de procéder
            profile = getattr(instance, 'profile', None)
            if profile is not None:  # Vérifiez si l'instance de profil existe déjà
                for key, value in profile_data.items():
                    setattr(profile, key, value)
                profile.save()
            else:
                # Créer un profil s'il n'existe pas - facultatif selon la logique métier
                UserProfile.objects.create(user=instance, **profile_data)

        return instance

