from django.shortcuts import render
from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from .models import (
    Category, Resource, Disorder, Symptom, 
    Specialty, Therapist, CrisisResource, 
    Statistic, Newsletter, UserProfile
)
from .serializers import (
    CategorySerializer, ResourceSerializer, DisorderSerializer,
    TherapistSerializer, CrisisResourceSerializer, StatisticSerializer,
    NewsletterSerializer, UserSerializer, UserProfileSerializer
)
from .services.podcast_service import PodcastService

# ViewSets
class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows categories to be viewed or edited.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

def index(request):
    """Main page view"""
    return render(request, 'base.html')

# API Viewsets
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

class ResourceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Resource.objects.all().order_by('-date_published')
    serializer_class = ResourceSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        queryset = Resource.objects.all().order_by('-date_published')
        resource_type = self.request.query_params.get('type', None)
        category = self.request.query_params.get('category', None)
        
        if resource_type:
            queryset = queryset.filter(type=resource_type)
        if category:
            queryset = queryset.filter(category__name=category)
            
        return queryset

class DisorderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Disorder.objects.all()
    serializer_class = DisorderSerializer
    permission_classes = [permissions.AllowAny]

class TherapistViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Therapist.objects.all()
    serializer_class = TherapistSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        queryset = Therapist.objects.all()
        specialty = self.request.query_params.get('specialty', None)
        location = self.request.query_params.get('location', None)
        
        if specialty:
            queryset = queryset.filter(specialties__name=specialty)
        if location:
            queryset = queryset.filter(location__icontains=location)
            
        return queryset

class CrisisResourceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CrisisResource.objects.all()
    serializer_class = CrisisResourceSerializer
    permission_classes = [permissions.AllowAny]

class StatisticViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Statistic.objects.all()
    serializer_class = StatisticSerializer
    permission_classes = [permissions.AllowAny]

# API Views for user management
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

# Newsletter subscription
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

# Save resource to user profile
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

# Search functionality
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def search(request):
    query = request.query_params.get('q', '')
    if not query:
        return Response({"error": "Query parameter 'q' is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Search in resources
    resources = Resource.objects.filter(title__icontains=query) | Resource.objects.filter(description__icontains=query)
    resource_serializer = ResourceSerializer(resources, many=True)
    
    # Search in disorders
    disorders = Disorder.objects.filter(name__icontains=query) | Disorder.objects.filter(description__icontains=query)
    disorder_serializer = DisorderSerializer(disorders, many=True)
    
    # Search in therapists
    therapists = Therapist.objects.filter(name__icontains=query) | Therapist.objects.filter(bio__icontains=query)
    therapist_serializer = TherapistSerializer(therapists, many=True)
    
    return Response({
        "resources": resource_serializer.data,
        "disorders": disorder_serializer.data,
        "therapists": therapist_serializer.data
    })

# Podcast views
class PodcastViewSet(APIView):
    """
    API view for retrieving mental health podcasts from Podcast Index
    """
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, format=None):
        """
        Get mental health podcasts
        """
        podcast_service = PodcastService()
        category = request.query_params.get('category', 'popular')
        max_results = int(request.query_params.get('max_results', 10))
        
        try:
            podcasts = podcast_service.get_mental_health_podcasts(category, max_results)
            return Response(podcasts)
        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": f"Error retrieving podcasts: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def search_podcasts(request):
    """
    Search for mental health podcasts
    """
    query = request.query_params.get('q', '')
    max_results = int(request.query_params.get('max_results', 10))
    
    if not query:
        return Response(
            {"error": "Query parameter 'q' is required"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    podcast_service = PodcastService()
    podcasts = podcast_service.search_podcasts(query, max_results)
    return Response(podcasts)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_podcast_episodes(request, podcast_id):
    """
    Get episodes for a specific podcast
    """
    max_results = int(request.query_params.get('max_results', 10))
    
    podcast_service = PodcastService()
    episodes = podcast_service.get_podcast_episodes(podcast_id, max_results)
    return Response(episodes)
