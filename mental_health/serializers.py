from rest_framework import serializers
from .models import (
    Category, Resource, Disorder, Symptom, 
    Specialty, Therapist, CrisisResource, 
    Statistic, Newsletter, UserProfile
)
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class SymptomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symptom
        fields = ['name']

class DisorderSerializer(serializers.ModelSerializer):
    symptoms = SymptomSerializer(many=True, read_only=True)
    
    class Meta:
        model = Disorder
        fields = ['id', 'name', 'description', 'icon', 'symptoms']

class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ['name']

class ResourceSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Resource
        fields = [
            'id', 'title', 'description', 'type', 'category', 'category_name',
            'image', 'image_url', 'rating', 'read_time', 'duration', 
            'views', 'listens', 'date_published', 'content', 'external_url'
        ]

class TherapistSerializer(serializers.ModelSerializer):
    specialties = SpecialtySerializer(many=True, read_only=True)
    
    class Meta:
        model = Therapist
        fields = [
            'id', 'name', 'title', 'specialties', 'location',
            'image', 'image_url', 'bio', 'email', 'phone'
        ]

class CrisisResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrisisResource
        fields = ['id', 'name', 'number', 'description']

class StatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistic
        fields = ['id', 'value', 'description']

class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = ['email']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    saved_resources = ResourceSerializer(many=True, read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['user', 'bio', 'profile_picture', 'saved_resources']
