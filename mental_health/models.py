from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, help_text="Font Awesome icon name")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

class Resource(models.Model):
    RESOURCE_TYPES = (
        ('article', 'Article'),
        ('video', 'Video'),
        ('podcast', 'Podcast'),
        ('app', 'App'),
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='resources')
    image = models.ImageField(upload_to='resources/', null=True, blank=True)
    image_url = models.URLField(blank=True, null=True, help_text="External URL for image if not uploaded")
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    read_time = models.PositiveIntegerField(null=True, blank=True, help_text="Read time in minutes (for articles)")
    duration = models.PositiveIntegerField(null=True, blank=True, help_text="Duration in minutes (for videos/podcasts)")
    views = models.PositiveIntegerField(default=0, help_text="Number of views (for videos)")
    listens = models.PositiveIntegerField(default=0, help_text="Number of listens (for podcasts)")
    date_published = models.DateField()
    content = models.TextField(blank=True, help_text="Full content for articles")
    external_url = models.URLField(blank=True, null=True, help_text="URL for external content (videos, podcasts, etc.)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class Disorder(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="Font Awesome icon name")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class Symptom(models.Model):
    name = models.CharField(max_length=100)
    disorder = models.ForeignKey(Disorder, on_delete=models.CASCADE, related_name='symptoms')
    
    def __str__(self):
        return self.name

class Specialty(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Specialties"

class Therapist(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    specialties = models.ManyToManyField(Specialty, related_name='therapists')
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to='therapists/', null=True, blank=True)
    image_url = models.URLField(blank=True, null=True, help_text="External URL for image if not uploaded")
    bio = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class CrisisResource(models.Model):
    name = models.CharField(max_length=200)
    number = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class Statistic(models.Model):
    value = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.value} - {self.description}"

class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.email

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    saved_resources = models.ManyToManyField(Resource, blank=True, related_name='saved_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.username
