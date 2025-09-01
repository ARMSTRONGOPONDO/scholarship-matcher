from django.core.management.base import BaseCommand
from django.utils import timezone
from mental_health.services.podcast_service import PodcastService
from mental_health.models import Resource, Category
import json
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Fetch the latest mental health podcasts and episodes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            action='store_true',
            help='Output results to JSON file instead of saving to database',
        )
        parser.add_argument(
            '--count',
            type=int,
            default=5,
            help='Number of podcasts to fetch',
        )
        parser.add_argument(
            '--type',
            type=str,
            choices=['popular', 'trending', 'recent', 'all'],
            default='popular',
            help='Type of podcasts to fetch: popular, trending, recent, or all',
        )

    def handle(self, *args, **kwargs):
        output_to_file = kwargs['output']
        count = kwargs['count']
        podcast_type = kwargs['type']
        
        self.stdout.write(self.style.SUCCESS(f'Fetching {count} {podcast_type} podcasts...'))
        
        # Initialize the podcast service
        podcast_service = PodcastService()
        
        # Create output directory if outputting to file
        if output_to_file:
            output_dir = os.path.join(settings.BASE_DIR, 'media', 'podcasts')
            os.makedirs(output_dir, exist_ok=True)
            
            # Timestamp for the file
            timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
        
        # Fetch all types if requested
        if podcast_type == 'all':
            # Fetch popular podcasts
            self.stdout.write('Fetching popular podcasts...')
            popular_podcasts = podcast_service.get_mental_health_podcasts('popular', count)
            
            if output_to_file:
                self.save_to_json(popular_podcasts, f'popular_podcasts_{timestamp}.json')
                self.save_to_json(popular_podcasts, 'popular_podcasts_latest.json')
            else:
                self.save_to_database(popular_podcasts, podcast_service)
            
            # Fetch trending episodes
            self.stdout.write('Fetching trending episodes...')
            trending_episodes = podcast_service.get_mental_health_podcasts('trending', count)
            
            if output_to_file:
                self.save_to_json(trending_episodes, f'trending_episodes_{timestamp}.json')
                self.save_to_json(trending_episodes, 'trending_episodes_latest.json')
            
            # Fetch recent episodes
            self.stdout.write('Fetching recent episodes...')
            recent_episodes = podcast_service.get_mental_health_podcasts('recent', count)
            
            if output_to_file:
                self.save_to_json(recent_episodes, f'recent_episodes_{timestamp}.json')
                self.save_to_json(recent_episodes, 'recent_episodes_latest.json')
            
            return
        
        # Fetch podcasts based on type
        podcasts = podcast_service.get_mental_health_podcasts(podcast_type, count)
        
        if not podcasts:
            self.stdout.write(self.style.WARNING(f'No {podcast_type} podcasts/episodes found.'))
            return
        
        self.stdout.write(self.style.SUCCESS(f'Found {len(podcasts)} {podcast_type} podcasts/episodes'))
        
        # Save to file or database
        if output_to_file:
            filename = f'{podcast_type}_{timestamp}.json'
            self.save_to_json(podcasts, filename)
            self.save_to_json(podcasts, f'{podcast_type}_latest.json')
        else:
            self.save_to_database(podcasts, podcast_service)
    
    def save_to_json(self, data, filename):
        """Save data to a JSON file"""
        output_dir = os.path.join(settings.BASE_DIR, 'media', 'podcasts')
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        self.stdout.write(self.style.SUCCESS(f'Saved data to {filepath}'))
    
    def save_to_database(self, podcasts, podcast_service):
        """Save podcasts to the database"""
        # Create podcast category if it doesn't exist
        podcast_category, created = Category.objects.get_or_create(
            name='Podcasts',
            defaults={'icon': 'headphones'}
        )
        
        counter = 0
        for podcast in podcasts:
            # For episodes, we need to handle differently
            if 'enclosure_url' in podcast:
                # This is an episode
                title = podcast.get('title', '')
                description = podcast.get('description', '')
                podcast_title = podcast.get('podcast_title', 'Mental Health Podcast')
                
                # Check if resource already exists
                if Resource.objects.filter(title=title, type='podcast_episode').exists():
                    continue
                
                # Create resource
                Resource.objects.create(
                    title=title,
                    description=description,
                    type='podcast_episode',
                    category=podcast_category,
                    image_url=podcast.get('image', ''),
                    rating=4.0,  # Default rating
                    url=podcast.get('enclosure_url', ''),
                    author=podcast_title,
                    content_type='audio',
                    metadata={
                        'podcast_title': podcast_title,
                        'audio_url': podcast.get('enclosure_url', ''),
                        'duration': podcast.get('duration', 0),
                        'date_published': podcast.get('date_published', 0)
                    },
                    date_published=timezone.now().date()
                )
                counter += 1
            else:
                # This is a podcast
                title = podcast.get('title', '')
                description = podcast.get('description', '')
                
                # Check if resource already exists
                if Resource.objects.filter(title=title, type='podcast').exists():
                    continue
                
                # Get recent episodes
                episodes = podcast_service.get_podcast_episodes(podcast['id'], max_results=1)
                
                if not episodes:
                    continue
                    
                episode = episodes[0]
                
                # Create resource
                Resource.objects.create(
                    title=title,
                    description=description,
                    type='podcast',
                    category=podcast_category,
                    image_url=podcast.get('image', ''),
                    rating=4.5,  # Default rating
                    url=podcast.get('feed_url', ''),
                    author=podcast.get('author', ''),
                    content_type='audio',
                    metadata={
                        'podcast_id': podcast.get('id', ''),
                        'episode_count': podcast.get('episode_count', 0),
                        'latest_episode': {
                            'title': episode.get('title', ''),
                            'description': episode.get('description', ''),
                            'audio_url': episode.get('enclosure_url', ''),
                            'duration': episode.get('duration', 0)
                        }
                    },
                    date_published=timezone.now().date()
                )
                counter += 1
        
        self.stdout.write(self.style.SUCCESS(f'Added {counter} new podcasts/episodes to the database'))