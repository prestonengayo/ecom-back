from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from Back.serializers.user_serializer import UserSerializer, UserProfileSerializer
from Back.perm import IsAdmin

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_queryset(self):
        if self.request.user.profile.is_admin:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

    def create(self, request, *args, **kwargs):
        user_data = request.data.copy()
        profile_data = {
            'address': user_data.pop('profile.address', None),
            'phone': user_data.pop('profile.phone', None),
            'profile_image': request.FILES.get('profile.profile_image'),
        }

        user_serializer = self.get_serializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        profile_data['user'] = user.id
        profile_serializer = UserProfileSerializer(data=profile_data)
        profile_serializer.is_valid(raise_exception=True)
        profile_serializer.save()

        headers = self.get_success_headers(user_serializer.data)
        return Response(user_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
