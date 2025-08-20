from django.shortcuts import render
from rest_framework import viewsets, permissions

from ..models import (
    Category, Resource, Disorder, 
    Therapist, CrisisResource, Statistic
)
from ..serializers import (
    CategorySerializer, ResourceSerializer, DisorderSerializer,
    TherapistSerializer, CrisisResourceSerializer, StatisticSerializer
)

def index(request):
    """Main page view"""
    return render(request, 'base.html')

class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows categories to be viewed or edited.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

class ResourceViewSet(viewsets.ModelViewSet):
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

class DisorderViewSet(viewsets.ModelViewSet):
    queryset = Disorder.objects.all()
    serializer_class = DisorderSerializer
    permission_classes = [permissions.AllowAny]

class TherapistViewSet(viewsets.ModelViewSet):
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

class CrisisResourceViewSet(viewsets.ModelViewSet):
    queryset = CrisisResource.objects.all()
    serializer_class = CrisisResourceSerializer
    permission_classes = [permissions.AllowAny]

class StatisticViewSet(viewsets.ModelViewSet):
    queryset = Statistic.objects.all()
    serializer_class = StatisticSerializer
    permission_classes = [permissions.AllowAny]
