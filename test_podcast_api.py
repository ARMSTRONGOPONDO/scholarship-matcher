#!/usr/bin/env python3
"""
Test script for Podcast Index API integration

This script tests the connection to the Podcast Index API and demonstrates
fetching mental health related podcasts and episodes.

Usage:
    python test_podcast_api.py [--api-key KEY] [--api-secret SECRET]
    
Environment variables:
    PODCAST_INDEX_API_KEY - Your Podcast Index API key
    PODCAST_INDEX_API_SECRET - Your Podcast Index API secret

Django integration:
    Can also be run within Django context to test the PodcastService class
"""

import os
import sys
import json
import argparse
from pathlib import Path

# Add the project root to Python path for Django imports
project_root = Path(__file__).parent
sys.path.append(str(project_root))

def test_api_standalone(api_key, api_secret):
    """Test API with standalone implementation (no Django)"""
    import requests
    import hashlib
    import hmac
    import time
    
    print("Testing Podcast Index API connection (standalone)...")
    print(f"API Key: {api_key[:8]}...")
    
    # Generate authentication headers
    epoch_time = int(time.time())
    data = api_key + api_secret + str(epoch_time)
    sha1hash = hashlib.sha1(data.encode()).hexdigest()
    
    headers = {
        'X-Auth-Date': str(epoch_time),
        'X-Auth-Key': api_key,
        'Authorization': sha1hash,
        'User-Agent': 'MentalHealthPlatform-Test/1.0'
    }
    
    try:
        # Test basic connection
        print("\\n1. Testing basic connection...")
        response = requests.get(
            "https://api.podcastindex.org/api/1.0/categories/list",
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        categories = response.json()
        print(f"✅ Connection successful! Found {len(categories.get('feeds', []))} categories")
        
        # Test mental health podcast search
        print("\\n2. Searching for mental health podcasts...")
        response = requests.get(
            "https://api.podcastindex.org/api/1.0/search/byterm",
            headers=headers,
            params={'q': 'mental health', 'max': 5, 'clean': 'true'},
            timeout=30
        )
        response.raise_for_status()
        
        search_results = response.json()
        podcasts = search_results.get('feeds', [])
        print(f"✅ Found {len(podcasts)} mental health podcasts")
        
        # Display some results
        for i, podcast in enumerate(podcasts[:3], 1):
            print(f"\\n   Podcast {i}:")
            print(f"   Title: {podcast.get('title', 'N/A')}")
            print(f"   Author: {podcast.get('author', 'N/A')}")
            print(f"   Episodes: {podcast.get('episodeCount', 'N/A')}")
            print(f"   Description: {podcast.get('description', 'N/A')[:100]}...")
            
        # Test getting recent episodes
        print("\\n3. Getting recent mental health episodes...")
        response = requests.get(
            "https://api.podcastindex.org/api/1.0/recent/episodes",
            headers=headers,
            params={'max': 3, 'fulltext': 'mental health OR therapy OR anxiety'},
            timeout=30
        )
        response.raise_for_status()
        
        recent_results = response.json()
        episodes = recent_results.get('items', [])
        print(f"✅ Found {len(episodes)} recent episodes")
        
        for i, episode in enumerate(episodes[:2], 1):
            print(f"\\n   Episode {i}:")
            print(f"   Title: {episode.get('title', 'N/A')}")
            print(f"   Podcast: {episode.get('feedTitle', 'N/A')}")
            print(f"   Duration: {episode.get('duration', 'N/A')} seconds")
            print(f"   Published: {episode.get('datePublishedPretty', 'N/A')}")
            
        # Test getting episodes for a specific podcast
        if podcasts:
            podcast_id = podcasts[0].get('id')
            if podcast_id:
                print(f"\\n4. Getting episodes for podcast ID {podcast_id}...")
                response = requests.get(
                    "https://api.podcastindex.org/api/1.0/episodes/byfeedid",
                    headers=headers,
                    params={'id': podcast_id, 'max': 2},
                    timeout=30
                )
                response.raise_for_status()
                
                episodes_results = response.json()
                podcast_episodes = episodes_results.get('items', [])
                print(f"✅ Found {len(podcast_episodes)} episodes for this podcast")
                
                for i, episode in enumerate(podcast_episodes[:1], 1):
                    print(f"\\n   Episode {i}:")
                    print(f"   Title: {episode.get('title', 'N/A')}")
                    print(f"   Audio URL: {episode.get('enclosureUrl', 'N/A')}")
                    print(f"   Duration: {episode.get('duration', 'N/A')} seconds")
                    
        print("\\n✅ All tests passed!")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ API request failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_api_django():
    """Test API using Django's PodcastService"""
    try:
        # Set up Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mental_health_core.settings')
        
        import django
        django.setup()
        
        from mental_health.services.podcast_service import PodcastService
        
        print("Testing Podcast Index API connection (Django integration)...")
        
        # Initialize service
        podcast_service = PodcastService()
        
        # Test connection
        print("\\n1. Testing connection...")
        success, message = podcast_service.test_connection()
        if success:
            print(f"✅ {message}")
        else:
            print(f"❌ {message}")
            return False
            
        # Test searching podcasts
        print("\\n2. Searching for mental health podcasts...")
        podcasts = podcast_service.get_mental_health_podcasts('popular', 3)
        print(f"✅ Found {len(podcasts)} popular podcasts")
        
        for i, podcast in enumerate(podcasts[:2], 1):
            print(f"\\n   Podcast {i}:")
            print(f"   Title: {podcast.get('title', 'N/A')}")
            print(f"   Author: {podcast.get('author', 'N/A')}")
            print(f"   Episodes: {podcast.get('episodeCount', 'N/A')}")
            
        # Test getting recent episodes
        print("\\n3. Getting recent episodes...")
        episodes = podcast_service.get_mental_health_podcasts('recent', 2)
        print(f"✅ Found {len(episodes)} recent episodes")
        
        for i, episode in enumerate(episodes[:1], 1):
            print(f"\\n   Episode {i}:")
            print(f"   Title: {episode.get('title', 'N/A')}")
            print(f"   Podcast: {episode.get('feedTitle', 'N/A')}")
            
        print("\\n✅ Django integration tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Django test failed: {e}")
        return False

def get_credentials(args):
    """Get API credentials from arguments, env, or Django settings"""
    api_key = args.api_key
    api_secret = args.api_secret
    
    # Try environment variables
    if not api_key:
        api_key = os.getenv('PODCAST_INDEX_API_KEY')
    if not api_secret:
        api_secret = os.getenv('PODCAST_INDEX_API_SECRET')
        
    # Try loading from .env file
    if not api_key or not api_secret:
        env_file = project_root / '.env'
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('PODCAST_INDEX_API_KEY='):
                        api_key = api_key or line.split('=', 1)[1]
                    elif line.startswith('PODCAST_INDEX_API_SECRET='):
                        api_secret = api_secret or line.split('=', 1)[1]
    
    # Try Django settings
    if not api_key or not api_secret:
        try:
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mental_health_core.settings')
            import django
            django.setup()
            from django.conf import settings
            
            api_key = api_key or getattr(settings, 'PODCAST_INDEX_API_KEY', None)
            api_secret = api_secret or getattr(settings, 'PODCAST_INDEX_API_SECRET', None)
            
        except Exception as e:
            print(f"Warning: Could not load Django settings: {e}")
    
    return api_key, api_secret

def main():
    parser = argparse.ArgumentParser(description='Test Podcast Index API integration')
    parser.add_argument('--api-key', help='Podcast Index API Key')
    parser.add_argument('--api-secret', help='Podcast Index API Secret')
    parser.add_argument('--django', action='store_true', help='Test Django integration')
    parser.add_argument('--standalone', action='store_true', help='Test standalone implementation')
    parser.add_argument('--save-results', help='Save results to JSON file')
    
    args = parser.parse_args()
    
    # If no specific test is requested, run both
    if not args.django and not args.standalone:
        args.django = True
        args.standalone = True
    
    print("🧠 Mental Health Platform - Podcast API Test")
    print("=" * 50)
    
    success = True
    
    if args.standalone:
        api_key, api_secret = get_credentials(args)
        
        if not api_key or not api_secret:
            print("❌ API credentials not found!")
            print("\\nPlease provide credentials via:")
            print("  1. Command line: --api-key KEY --api-secret SECRET")
            print("  2. Environment variables: PODCAST_INDEX_API_KEY, PODCAST_INDEX_API_SECRET")
            print("  3. .env file in project root")
            print("  4. Django settings")
            return 1
            
        success &= test_api_standalone(api_key, api_secret)
        
    if args.django:
        print("\\n" + "="*50)
        success &= test_api_django()
    
    if success:
        print("\\n🎉 All tests completed successfully!")
        return 0
    else:
        print("\\n💥 Some tests failed. Check your API credentials and connection.")
        return 1

if __name__ == '__main__':
    exit(main())