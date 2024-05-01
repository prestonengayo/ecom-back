from django.contrib.auth.models import User
from rest_framework import serializers
from Back.models.user import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['address', 'phone', 'profile_image']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=True)

    class Meta:
        model = User
        fields = ['id','username', 'email', 'password','last_name','first_name', 'profile']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.pop('first_name', ''),
            last_name=validated_data.pop('last_name', '')
        )
        # Créez UserProfile ici seulement si vous ne le faites pas dans le signal
        UserProfile.objects.get_or_create(user=user, defaults=profile_data)
        return user


    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)  # Utilisez None comme valeur par défaut
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        
        # Mise à jour du profil si les données de profil sont fournies
        if profile_data:
            profile = getattr(instance, 'profile', None)
            if profile is not None:
                for key, value in profile_data.items():
                    setattr(profile, key, value)
                profile.save()

        return instance

