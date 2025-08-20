from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from ..models import UserProfile, Newsletter, Resource
from ..serializers import (
    UserSerializer, UserProfileSerializer,
    NewsletterSerializer
)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Create user profile
        UserProfile.objects.create(user=user)
        
        # Create token
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token.key
        })

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "user": UserSerializer(user).data,
                "token": token.key
            })
        return Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user.profile

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def subscribe_newsletter(request):
    serializer = NewsletterSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        # Check if email already exists
        if Newsletter.objects.filter(email=email).exists():
            return Response({"message": "Email already subscribed"}, status=status.HTTP_200_OK)
        
        serializer.save()
        return Response({"message": "Successfully subscribed to newsletter"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def save_resource(request, resource_id):
    try:
        resource = Resource.objects.get(id=resource_id)
        profile = request.user.profile
        
        if resource in profile.saved_resources.all():
            profile.saved_resources.remove(resource)
            return Response({"message": "Resource removed from saved items"}, status=status.HTTP_200_OK)
        else:
            profile.saved_resources.add(resource)
            return Response({"message": "Resource saved successfully"}, status=status.HTTP_200_OK)
    except Resource.DoesNotExist:
        return Response({"error": "Resource not found"}, status=status.HTTP_404_NOT_FOUND)
