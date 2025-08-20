from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *  # All views are properly exposed in views/__init__.py

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'resources', ResourceViewSet)
router.register(r'disorders', DisorderViewSet)
router.register(r'therapists', TherapistViewSet)
router.register(r'crisis-resources', CrisisResourceViewSet)
router.register(r'statistics', StatisticViewSet)

urlpatterns = [
    # Main page view
    path('', index, name='index'),
    
    # API root
    path('api/', include(router.urls)),
    
    # Podcast API endpoints
    path('api/podcasts/', PodcastViewSet.as_view(), name='podcasts'),
    path('api/podcasts/search/', search_podcasts, name='search-podcasts'),
    path('api/podcasts/<int:podcast_id>/episodes/', get_podcast_episodes, name='podcast-episodes'),
    
    # User management endpoints
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/profile/', UserProfileView.as_view(), name='user-profile'),
    
    # Newsletter subscription
    path('api/newsletter/subscribe/', subscribe_newsletter, name='subscribe-newsletter'),
    
    # Save resource to user profile
    path('api/resources/<int:resource_id>/save/', save_resource, name='save-resource'),
    
    # Search endpoint
    path('api/search/', search, name='search'),
]
