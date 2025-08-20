from django.core.management.base import BaseCommand
from mental_health.services.podcast_service import PodcastService
from mental_health.models import Resource, Category
import json
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Load initial podcast data from Podcast Index API'

    def add_arguments(self, parser):
        parser.add_argument(
            '--save-json',
            action='store_true',
            help='Save results to JSON files for testing/debugging'
        )
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Number of podcasts to load'
        )

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting to load podcast data...'))
        
        save_json = kwargs.get('save_json', False)
        count = kwargs.get('count', 10)
        
        # Create podcast category if it doesn't exist
        podcast_category, created = Category.objects.get_or_create(
            name='Podcasts',
            defaults={'icon': 'headphones'}
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('Created "Podcasts" category'))
        
        # Get mental health podcasts
        podcast_service = PodcastService()
        
        # Get popular podcasts
        self.stdout.write('Loading popular mental health podcasts...')
        popular_podcasts = podcast_service.get_mental_health_podcasts('popular', count)
        
        if not popular_podcasts:
            self.stdout.write(self.style.WARNING('No popular podcasts found. Check your API key and connection.'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Found {len(popular_podcasts)} popular podcasts'))
            
            # Save to database
            self.save_podcasts_to_db(popular_podcasts, podcast_service, podcast_category)
            
            # Save to JSON if requested
            if save_json:
                self.save_to_json(popular_podcasts, 'popular_podcasts.json')
        
        # Get recent episodes
        self.stdout.write('Loading recent mental health podcast episodes...')
        recent_episodes = podcast_service.get_mental_health_podcasts('recent', count)
        
        if not recent_episodes:
            self.stdout.write(self.style.WARNING('No recent episodes found.'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Found {len(recent_episodes)} recent episodes'))
            
            # Save to JSON if requested
            if save_json:
                self.save_to_json(recent_episodes, 'recent_episodes.json')
        
        self.stdout.write(self.style.SUCCESS('Finished loading podcast data'))
    
    def save_podcasts_to_db(self, podcasts, podcast_service, podcast_category):
        counter = 0
        for podcast in podcasts:
            # Check if podcast already exists
            if Resource.objects.filter(title=podcast['title'], type='podcast').exists():
                continue
                
            # Get recent episodes
            episodes = podcast_service.get_podcast_episodes(podcast['id'], max_results=1)
            
            if not episodes:
                continue
                
            episode = episodes[0]
            
            # Create resource
            Resource.objects.create(
                title=podcast['title'],
                description=podcast['description'],
                type='podcast',
                category=podcast_category,
                image_url=podcast['image'],
                rating=4.5,  # Default rating
                url=podcast['feed_url'],
                author=podcast['author'],
                content_type='audio',
                metadata={
                    'podcast_id': podcast['id'],
                    'episode_count': podcast['episode_count'],
                    'latest_episode': {
                        'title': episode['title'],
                        'description': episode['description'],
                        'audio_url': episode['enclosure_url'],
                        'duration': episode['duration']
                    }
                }
            )
            counter += 1
        
        self.stdout.write(self.style.SUCCESS(f'Added {counter} new podcasts to the database'))
    
    def save_to_json(self, data, filename):
        output_dir = os.path.join(settings.BASE_DIR, 'media', 'podcasts')
        os.makedirs(output_dir, exist_ok=True)
        
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        self.stdout.write((self.style.SUCCESS(f'Saved data to {filepath}'))
                duration=episode['duration'] // 60 if episode['duration'] else 30,  # Convert seconds to minutes
                listens=1000,  # Default listens
                date_published=episode['date_published'],
                content=f"Author: {podcast['author']}\n\nLatest Episode: {episode['title']}\n\n{episode['description']}",
                external_url=episode['enclosure_url']
            )
            counter += 1
            
        self.stdout.write(self.style.SUCCESS(f'Successfully loaded {counter} podcasts'))
