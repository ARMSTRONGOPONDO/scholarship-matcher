import time
import hashlib
import requests
import podcastindex
from django.conf import settings

class PodcastService:
    """
    Service for interacting with the Podcast Index API.
    This service provides methods to search, fetch and filter podcasts
    relevant to mental health topics.
    """
    
    def __init__(self):
        """Initialize the Podcast Index API client"""
        config = {
            "api_key": settings.PODCAST_INDEX_API['API_KEY'],
            "api_secret": settings.PODCAST_INDEX_API['API_SECRET'],
            "user_agent": settings.PODCAST_INDEX_API['USER_AGENT']
        }
        self.api = podcastindex.init(config)
    
    def search_podcasts(self, query, max_results=10):
        """
        Search for podcasts by query term
        
        Args:
            query (str): Search term
            max_results (int): Maximum number of results to return
            
        Returns:
            list: List of podcast dictionaries
        """
        try:
            results = self.api.search(query)
            
            if 'feeds' not in results or not results['feeds']:
                return []
            
            podcasts = results['feeds'][:max_results]
            
            # Clean and format the response
            formatted_podcasts = []
            for podcast in podcasts:
                formatted_podcasts.append({
                    'id': podcast.get('id'),
                    'title': podcast.get('title'),
                    'description': podcast.get('description'),
                    'image': podcast.get('artwork') or podcast.get('image'),
                    'author': podcast.get('author'),
                    'website': podcast.get('link'),
                    'feed_url': podcast.get('url'),
                    'categories': podcast.get('categories', {}),
                    'episode_count': podcast.get('episodeCount', 0),
                })
            
            return formatted_podcasts
        except Exception as e:
            print(f"Error searching podcasts: {str(e)}")
            return []
    
    def get_podcast_episodes(self, podcast_id, max_results=10):
        """
        Get episodes for a specific podcast
        
        Args:
            podcast_id (int): Podcast ID from the Podcast Index
            max_results (int): Maximum number of episodes to return
            
        Returns:
            list: List of episode dictionaries
        """
        try:
            results = self.api.episodesByFeedId(podcast_id)
            
            if 'items' not in results or not results['items']:
                return []
            
            episodes = results['items'][:max_results]
            
            # Clean and format the response
            formatted_episodes = []
            for episode in episodes:
                formatted_episodes.append({
                    'id': episode.get('id'),
                    'title': episode.get('title'),
                    'description': episode.get('description') or '',
                    'link': episode.get('link'),
                    'podcast_title': episode.get('feedTitle', ''),
                    'enclosure_url': episode.get('enclosureUrl'),  # Audio file URL
                    'enclosure_type': episode.get('enclosureType'),
                    'duration': episode.get('duration', 0),
                    'date_published': episode.get('datePublished'),
                    'image': episode.get('image') or episode.get('feedImage'),
                    'explicit': episode.get('explicit', 0) == 1,
                })
            
            return formatted_episodes
        except Exception as e:
            print(f"Error getting podcast episodes: {str(e)}")
            return []
    
    def get_mental_health_podcasts(self, category='recent', max_results=10):
        """
        Get mental health podcasts by category
        
        Args:
            category (str): Category of podcasts to fetch:
                - 'recent': Recent episodes from mental health podcasts
                - 'popular': Popular mental health podcasts
                - 'trending': Trending mental health podcasts
            max_results (int): Maximum number of results to return
            
        Returns:
            list: List of podcast/episode dictionaries depending on category
        """
        try:
            if category == 'recent':
                # Get recent episodes from mental health podcasts
                # First search for some mental health podcasts
                mental_health_terms = [
                    "mental health", "psychology", "therapy", "depression", 
                    "anxiety", "mindfulness", "self care", "wellbeing", "wellness"
                ]
                
                # Use a random term to get variety
                import random
                search_term = random.choice(mental_health_terms)
                
                # Get podcasts first
                podcasts = self.search_podcasts(search_term, max_results=5)
                
                # Get episodes from each podcast
                all_episodes = []
                for podcast in podcasts:
                    episodes = self.get_podcast_episodes(podcast['id'], max_results=3)
                    for episode in episodes:
                        # Add podcast information to episode
                        if not episode.get('podcast_title'):
                            episode['podcast_title'] = podcast['title']
                        if not episode.get('image'):
                            episode['image'] = podcast['image']
                        all_episodes.append(episode)
                
                # Sort by date (most recent first)
                all_episodes.sort(key=lambda x: x.get('date_published', 0), reverse=True)
                
                return all_episodes[:max_results]
            
            elif category == 'popular':
                # Get popular mental health podcasts
                # We'll use the trending API and filter for mental health topics
                trending = self.api.trending(max=50)
                
                if 'feeds' not in trending or not trending['feeds']:
                    return []
                
                # Filter for mental health keywords in title or description
                mental_health_keywords = [
                    'mental', 'health', 'therapy', 'psychology', 'depression', 
                    'anxiety', 'mindful', 'wellness', 'well-being', 'self-care', 'counseling'
                ]
                
                mental_health_podcasts = []
                for podcast in trending['feeds']:
                    title = podcast.get('title', '').lower()
                    description = podcast.get('description', '').lower()
                    
                    # Check if any keyword is in title or description
                    if any(keyword in title or keyword in description for keyword in mental_health_keywords):
                        mental_health_podcasts.append({
                            'id': podcast.get('id'),
                            'title': podcast.get('title'),
                            'description': podcast.get('description'),
                            'image': podcast.get('artwork') or podcast.get('image'),
                            'author': podcast.get('author'),
                            'website': podcast.get('link'),
                            'feed_url': podcast.get('url'),
                            'categories': podcast.get('categories', {}),
                            'episode_count': podcast.get('episodeCount', 0),
                        })
                
                return mental_health_podcasts[:max_results]
            
            elif category == 'trending':
                # Get trending mental health episodes
                # First get episodes from the 'new episodes' API
                episodes = self.api.episodes(max=100)
                
                if 'items' not in episodes or not episodes['items']:
                    return []
                
                # Filter for mental health keywords in title or description
                mental_health_keywords = [
                    'mental', 'health', 'therapy', 'psychology', 'depression', 
                    'anxiety', 'mindful', 'wellness', 'well-being', 'self-care', 'counseling'
                ]
                
                mental_health_episodes = []
                for episode in episodes['items']:
                    title = episode.get('title', '').lower()
                    description = episode.get('description', '').lower()
                    
                    # Check if any keyword is in title or description
                    if any(keyword in title or keyword in description for keyword in mental_health_keywords):
                        mental_health_episodes.append({
                            'id': episode.get('id'),
                            'title': episode.get('title'),
                            'description': episode.get('description') or '',
                            'link': episode.get('link'),
                            'podcast_title': episode.get('feedTitle', ''),
                            'enclosure_url': episode.get('enclosureUrl'),
                            'enclosure_type': episode.get('enclosureType'),
                            'duration': episode.get('duration', 0),
                            'date_published': episode.get('datePublished'),
                            'image': episode.get('image') or episode.get('feedImage'),
                            'explicit': episode.get('explicit', 0) == 1,
                        })
                
                return mental_health_episodes[:max_results]
            
            else:
                raise ValueError(f"Invalid category: {category}. Must be 'recent', 'popular', or 'trending'")
        
        except Exception as e:
            print(f"Error getting mental health podcasts: {str(e)}")
            return []
    
    
    def get_trending_episodes(self, max_results=10):
        """
        Get trending mental health episodes
        
        Args:
            max_results (int): Maximum number of episodes to return
            
        Returns:
            list: List of episode dictionaries
        """
        try:
            # Get trending episodes across all categories
            results = self.api.episodes_trending()
            
            if 'items' not in results or not results['items']:
                return []
            
            # Filter for mental health related content
            mental_health_keywords = [
                "mental", "health", "therapy", "psychology", "mindful", 
                "meditation", "anxiety", "depression", "self-care", "wellness",
                "counseling", "stress", "trauma"
            ]
            
            mental_health_episodes = []
            for episode in results['items']:
                # Check if title or description contains mental health keywords
                title = episode.get('title', '').lower()
                description = episode.get('description', '').lower()
                
                if any(keyword in title or keyword in description for keyword in mental_health_keywords):
                    mental_health_episodes.append({
                        'id': episode.get('id'),
                        'title': episode.get('title'),
                        'description': episode.get('description'),
                        'link': episode.get('link'),
                        'enclosure_url': episode.get('enclosureUrl'),
                        'enclosure_type': episode.get('enclosureType'),
                        'duration': episode.get('duration', 0),
                        'date_published': episode.get('datePublished'),
                        'image': episode.get('image'),
                        'podcast_title': episode.get('feedTitle'),
                        'explicit': episode.get('explicit', 0) == 1,
                    })
            
            return mental_health_episodes[:max_results]
        except Exception as e:
            print(f"Error getting trending episodes: {str(e)}")
            return []
    
    def get_recent_episodes(self, max_results=10):
        """
        Get recent mental health episodes
        
        Args:
            max_results (int): Maximum number of episodes to return
            
        Returns:
            list: List of episode dictionaries
        """
        try:
            # First, get popular mental health podcasts
            podcasts = self.get_mental_health_podcasts(5)
            
            # Then get recent episodes from these podcasts
            recent_episodes = []
            for podcast in podcasts:
                podcast_id = podcast['id']
                episodes = self.get_podcast_episodes(podcast_id, 3)  # Get 3 episodes per podcast
                for episode in episodes:
                    # Add podcast info to episode
                    episode['podcast_title'] = podcast['title']
                    episode['podcast_image'] = podcast['image']
                    recent_episodes.append(episode)
            
            # Sort by date published (newest first)
            recent_episodes.sort(key=lambda x: x.get('date_published', 0), reverse=True)
            
            return recent_episodes[:max_results]
        except Exception as e:
            print(f"Error getting recent episodes: {str(e)}")
            return []
