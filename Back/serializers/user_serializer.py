from django.contrib.auth.models import User
from rest_framework import serializers
from Back.models.user import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['address', 'phone', 'profile_image']
        extra_kwargs = {
            'address': {'required': False},
            'phone': {'required': False},
            'profile_image': {'required': False}
        }


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'profile']
        extra_kwargs = {
            'username': {'required': False},
            'email': {'required': False},
            'password': {'write_only': True, 'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'profile': {'required': False}
        }

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', {})
        user = User.objects.create_user(
            username=validated_data.get('username', ''),
            email=validated_data.get('email', ''),
            password=validated_data.get('password', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        UserProfile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        for key, value in validated_data.items():
            if key != 'password':  # Skip the password field for partial updates
                setattr(instance, key, value)

        if 'password' in validated_data:
            instance.set_password(validated_data['password'])

        instance.save()

        if profile_data:
            profile = instance.profile
            for key, value in profile_data.items():
                setattr(profile, key, value)
            profile.save()

        return instance

    def partial_update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        for key, value in validated_data.items():
            if key != 'password' and key != 'username':  # Skip the password and username fields for partial updates
                setattr(instance, key, value)

        if 'password' in validated_data:
            instance.set_password(validated_data['password'])

        instance.save()

        if profile_data:
            profile = instance.profile
            for key, value in profile_data.items():
                setattr(profile, key, value)
            profile.save()

        return instance
