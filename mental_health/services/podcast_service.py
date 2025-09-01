import requests
import hashlib
import hmac
import time
import os
from django.conf import settings


class PodcastService:
    """
    Service to interact with the Podcast Index API for mental health podcasts
    """
    
    def __init__(self):
        self.api_key = self._get_api_key()
        self.api_secret = self._get_api_secret()
        self.base_url = "https://api.podcastindex.org/api/1.0"
        
    def _get_api_key(self):
        """Get API key from various sources"""
        # Try environment variable first
        api_key = os.getenv('PODCAST_INDEX_API_KEY')
        if api_key:
            return api_key
            
        # Try Django settings
        try:
            return settings.PODCAST_INDEX_API_KEY
        except AttributeError:
            pass
            
        return None
        
    def _get_api_secret(self):
        """Get API secret from various sources"""
        # Try environment variable first
        api_secret = os.getenv('PODCAST_INDEX_API_SECRET')
        if api_secret:
            return api_secret
            
        # Try Django settings
        try:
            return settings.PODCAST_INDEX_API_SECRET
        except AttributeError:
            pass
            
        return None
        
    def _get_headers(self):
        """Generate authentication headers for API requests"""
        if not self.api_key or not self.api_secret:
            raise ValueError("API key and secret are required. Set PODCAST_INDEX_API_KEY and PODCAST_INDEX_API_SECRET environment variables.")
            
        epoch_time = int(time.time())
        data = self.api_key + self.api_secret + str(epoch_time)
        sha1hash = hashlib.sha1(data.encode()).hexdigest()
        
        return {
            'X-Auth-Date': str(epoch_time),
            'X-Auth-Key': self.api_key,
            'Authorization': sha1hash,
            'User-Agent': 'MentalHealthPlatform/1.0'
        }
        
    def search_podcasts(self, query="mental health", max_results=10):
        """Search for podcasts by term"""
        try:
            headers = self._get_headers()
            params = {
                'q': query,
                'max': max_results,
                'clean': 'true'
            }
            
            response = requests.get(
                f"{self.base_url}/search/byterm",
                headers=headers,
                params=params,
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            return data.get('feeds', [])
            
        except Exception as e:
            print(f"Error searching podcasts: {e}")
            return []
            
    def get_trending_podcasts(self, max_results=10):
        """Get trending podcasts"""
        try:
            headers = self._get_headers()
            params = {
                'max': max_results,
                'lang': 'en'
            }
            
            response = requests.get(
                f"{self.base_url}/podcasts/trending",
                headers=headers,
                params=params,
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            return data.get('feeds', [])
            
        except Exception as e:
            print(f"Error getting trending podcasts: {e}")
            return []
            
    def get_podcast_episodes(self, podcast_id, max_results=10):
        """Get episodes for a specific podcast"""
        try:
            headers = self._get_headers()
            params = {
                'id': podcast_id,
                'max': max_results
            }
            
            response = requests.get(
                f"{self.base_url}/episodes/byfeedid",
                headers=headers,
                params=params,
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            return data.get('items', [])
            
        except Exception as e:
            print(f"Error getting podcast episodes: {e}")
            return []
            
    def get_recent_episodes(self, max_results=10):
        """Get recent episodes across all podcasts"""
        try:
            headers = self._get_headers()
            params = {
                'max': max_results,
                'fulltext': 'mental health OR anxiety OR depression OR therapy OR wellness'
            }
            
            response = requests.get(
                f"{self.base_url}/recent/episodes",
                headers=headers,
                params=params,
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            return data.get('items', [])
            
        except Exception as e:
            print(f"Error getting recent episodes: {e}")
            return []
            
    def get_mental_health_podcasts(self, type='popular', max_results=10):
        """
        Get mental health podcasts of different types
        
        Args:
            type: 'popular', 'trending', or 'recent'
            max_results: number of results to return
        """
        if type == 'popular':
            return self.search_podcasts("mental health therapy wellness", max_results)
        elif type == 'trending':
            # Filter trending for mental health content
            trending = self.get_trending_podcasts(max_results * 2)
            mental_health_trending = [
                pod for pod in trending 
                if any(keyword in pod.get('title', '').lower() or 
                      keyword in pod.get('description', '').lower()
                      for keyword in ['mental', 'health', 'therapy', 'anxiety', 'depression', 'wellness'])
            ]
            return mental_health_trending[:max_results]
        elif type == 'recent':
            return self.get_recent_episodes(max_results)
        else:
            return self.search_podcasts("mental health", max_results)
            
    def test_connection(self):
        """Test the API connection"""
        try:
            headers = self._get_headers()
            response = requests.get(
                f"{self.base_url}/categories/list",
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            return True, "Connection successful"
        except Exception as e:
            return False, str(e)