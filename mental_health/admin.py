from django.contrib import admin
# Register your models here.
from .models import (
    Category, Resource, Disorder, Symptom, 
    Specialty, Therapist, CrisisResource, 
    Statistic, Newsletter, UserProfile
)

# Register models with admin site
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')
    search_fields = ('name',)

class SymptomInline(admin.TabularInline):
    model = Symptom
    extra = 1

@admin.register(Disorder)
class DisorderAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    inlines = [SymptomInline]

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'category', 'rating', 'date_published')
    list_filter = ('type', 'category', 'date_published')
    search_fields = ('title', 'description', 'content')
    date_hierarchy = 'date_published'

@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Therapist)
class TherapistAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'location')
    list_filter = ('specialties',)
    search_fields = ('name', 'title', 'bio', 'location')
    filter_horizontal = ('specialties',)

@admin.register(CrisisResource)
class CrisisResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'description')
    search_fields = ('name', 'number', 'description')

@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    list_display = ('value', 'description')
    search_fields = ('value', 'description')

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at', 'is_active')
    list_filter = ('is_active', 'subscribed_at')
    search_fields = ('email',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__username', 'user__email', 'bio')
    filter_horizontal = ('saved_resources',)
