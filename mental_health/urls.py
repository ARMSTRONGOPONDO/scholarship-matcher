from django.urls import path, include
from rest_framework.routers import DefaultRouter

app_name = 'mental_health'

# API router for REST endpoints
router = DefaultRouter()
# Add viewsets here when created

urlpatterns = [
    # API endpoints
    path('api/', include(router.urls)),
    
    # Add other URL patterns here
]