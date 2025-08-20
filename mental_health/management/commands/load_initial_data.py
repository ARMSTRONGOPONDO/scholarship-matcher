from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.utils import timezone
from mental_health.models import (
    Category, Resource, Disorder, Symptom, 
    Specialty, Therapist, CrisisResource, 
    Statistic
)
from datetime import datetime

class Command(BaseCommand):
    help = 'Loads initial data for the mental health platform'

    def add_arguments(self, parser):
        parser.add_argument(
            '--skip-podcasts',
            action='store_true',
            help='Skip loading podcasts from API'
        )
        parser.add_argument(
            '--podcasts-count',
            type=int,
            default=5,
            help='Number of podcasts to load from API'
        )

    def handle(self, *args, **kwargs):
        self.stdout.write('Loading initial data...')
        
        # Create categories
        self.stdout.write('Creating categories...')
        articles = Category.objects.create(name='Articles', icon='book')
        videos = Category.objects.create(name='Videos', icon='video')
        podcasts = Category.objects.create(name='Podcasts', icon='headphones')
        apps = Category.objects.create(name='Apps', icon='mobile-alt')
        
        # Create resources
        self.stdout.write('Creating resources...')
        Resource.objects.create(
            title='Understanding Anxiety Disorders',
            description='Learn about different types of anxiety disorders, their symptoms, and evidence-based treatment approaches to manage anxiety effectively.',
            type='article',
            category=articles,
            image_url='https://images.unsplash.com/photo-1491841550275-ad7854e35ca6?q=80',
            rating=4.8,
            read_time=12,
            date_published=datetime(2023, 5, 15).date(),
        )
        
        Resource.objects.create(
            title='Mindfulness Meditation Guide',
            description='A 20-minute guided meditation session to help reduce stress and improve focus through mindfulness techniques.',
            type='video',
            category=videos,
            image_url='https://images.unsplash.com/photo-1506126613408-eca07ce68773?q=80',
            rating=4.9,
            duration=21,
            views=12400,
            date_published=datetime(2023, 4, 20).date(),
        )
        
        Resource.objects.create(
            title='Breaking the Stigma',
            description='Conversations with mental health experts about overcoming societal stigma around mental illness in everyday life.',
            type='podcast',
            category=podcasts,
            image_url='https://images.unsplash.com/photo-1516321318423-f06f85e504b3?q=80',
            rating=4.7,
            duration=48,
            listens=8200,
            date_published=datetime(2023, 4, 10).date(),
        )
        
        Resource.objects.create(
            title='Coping with Depression',
            description='Practical strategies for managing depressive symptoms and improving mood through daily habits and cognitive techniques.',
            type='article',
            category=articles,
            image_url='https://images.unsplash.com/photo-1584697964358-3e14ca57658b?q=80',
            rating=4.6,
            read_time=15,
            date_published=datetime(2023, 4, 22).date(),
        )
        
        # Create disorders and symptoms
        self.stdout.write('Creating disorders and symptoms...')
        
        depression = Disorder.objects.create(
            name='Depression',
            description='Persistent sadness, loss of interest, and low energy affecting daily life.',
            icon='cloud'
        )
        Symptom.objects.create(name='Low mood', disorder=depression)
        Symptom.objects.create(name='Loss of interest', disorder=depression)
        Symptom.objects.create(name='Fatigue', disorder=depression)
        Symptom.objects.create(name='Sleep disturbances', disorder=depression)
        
        anxiety = Disorder.objects.create(
            name='Anxiety Disorders',
            description='Excessive fear, worry, and physical symptoms like rapid heartbeat.',
            icon='wind'
        )
        Symptom.objects.create(name='Excessive worry', disorder=anxiety)
        Symptom.objects.create(name='Restlessness', disorder=anxiety)
        Symptom.objects.create(name='Muscle tension', disorder=anxiety)
        Symptom.objects.create(name='Panic attacks', disorder=anxiety)
        
        bipolar = Disorder.objects.create(
            name='Bipolar Disorder',
            description='Mood swings ranging from depressive lows to manic highs.',
            icon='balance-scale'
        )
        Symptom.objects.create(name='Mood swings', disorder=bipolar)
        Symptom.objects.create(name='Energy changes', disorder=bipolar)
        Symptom.objects.create(name='Sleep disturbances', disorder=bipolar)
        Symptom.objects.create(name='Risky behavior', disorder=bipolar)
        
        ptsd = Disorder.objects.create(
            name='PTSD',
            description='Persistent mental and emotional stress following a traumatic event.',
            icon='puzzle-piece'
        )
        Symptom.objects.create(name='Flashbacks', disorder=ptsd)
        Symptom.objects.create(name='Nightmares', disorder=ptsd)
        Symptom.objects.create(name='Hypervigilance', disorder=ptsd)
        Symptom.objects.create(name='Avoidance', disorder=ptsd)
        
        # Create specialties
        self.stdout.write('Creating specialties...')
        depression_spec = Specialty.objects.create(name='Depression')
        anxiety_spec = Specialty.objects.create(name='Anxiety')
        trauma_spec = Specialty.objects.create(name='Trauma')
        relationships_spec = Specialty.objects.create(name='Relationships')
        family_spec = Specialty.objects.create(name='Family Issues')
        grief_spec = Specialty.objects.create(name='Grief')
        stress_spec = Specialty.objects.create(name='Stress')
        transitions_spec = Specialty.objects.create(name='Life Transitions')
        
        # Create therapists
        self.stdout.write('Creating therapists...')
        therapist1 = Therapist.objects.create(
            name='Dr. Sarah Johnson',
            title='Licensed Clinical Psychologist',
            location='New York, NY',
            image_url='https://images.unsplash.com/photo-1559839734-2b71ea197ec2?q=80',
        )
        therapist1.specialties.add(depression_spec, anxiety_spec, trauma_spec)
        
        therapist2 = Therapist.objects.create(
            name='Michael Rodriguez',
            title='Licensed Marriage & Family Therapist',
            location='Los Angeles, CA',
            image_url='https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?q=80',
        )
        therapist2.specialties.add(relationships_spec, family_spec, grief_spec)
        
        therapist3 = Therapist.objects.create(
            name='Dr. Aisha Patel',
            title='Clinical Social Worker',
            location='Chicago, IL',
            image_url='https://images.unsplash.com/photo-1622253692010-333f2da6031d?q=80',
        )
        therapist3.specialties.add(anxiety_spec, stress_spec, transitions_spec)
        
        # Create crisis resources
        self.stdout.write('Creating crisis resources...')
        CrisisResource.objects.create(
            name='Suicide & Crisis Lifeline',
            number='988',
            description='24/7 support for anyone in suicidal crisis or emotional distress'
        )
        
        CrisisResource.objects.create(
            name='National Suicide Prevention Lifeline',
            number='1-800-273-TALK (8255)',
            description='Free and confidential support for people in distress'
        )
        
        CrisisResource.objects.create(
            name='Substance Abuse Helpline',
            number='1-800-662-HELP (4357)',
            description='Treatment referral and information service'
        )
        
        # Create statistics
        self.stdout.write('Creating statistics...')
        Statistic.objects.create(
            value='1 in 5',
            description='Adults experience mental illness each year'
        )
        
        Statistic.objects.create(
            value='50%',
            description='Of mental health conditions begin by age 14'
        )
        
        Statistic.objects.create(
            value='75%',
            description='Of mental illnesses are treatable with proper care'
        )
        
        Statistic.objects.create(
            value='17.3M',
            description='US adults experienced at least one major depressive episode'
        )
        
        # Load podcasts from API
        skip_podcasts = kwargs.get('skip_podcasts', False)
        podcasts_count = kwargs.get('podcasts_count', 5)
        
        if not skip_podcasts:
            self.stdout.write('Loading podcasts from Podcast Index API...')
            try:
                call_command('load_podcasts', count=podcasts_count)
                call_command('fetch_podcasts', type='recent', count=5, output=True)
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'Error loading podcasts: {str(e)}'))
        else:
            self.stdout.write(self.style.WARNING('Skipping podcast loading'))
        
        self.stdout.write(self.style.SUCCESS('Successfully loaded initial data.'))
