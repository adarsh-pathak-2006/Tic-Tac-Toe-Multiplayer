from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Profile
from rest_framework.views import APIView
from authentication.serializers import RegisterSerializer, ProfileSerializer, ProfileUpdateSerializer
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.generics import RetrieveDestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

class RegisterAPI(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serial=RegisterSerializer(data=request.data)
        if serial.is_valid():
            username=serial.validated_data['username']
            email=serial.validated_data['email']
            first_name=serial.validated_data['first_name']
            last_name=serial.validated_data['last_name']
            password=serial.validated_data['password']

            if User.objects.filter(Q(username=username) | Q(email=email)).exists():
                return Response({'message':'username or email already exists'}, status=400)
            user=User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name, password=password)
            Profile.objects.create(user=user)
            return Response({'message':'profile and user created'}, status=201)
        return Response(serial.errors, status=400)


class MyProfileAPI(RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated]
    def get_serializer_class(self):
        if self.request.method=='GET':
            return ProfileSerializer
        return ProfileUpdateSerializer

    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)


class ProfileAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class=ProfileSerializer
    queryset=Profile.objects.all()
    



