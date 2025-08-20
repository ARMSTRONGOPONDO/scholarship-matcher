#!/usr/bin/env python
"""
Test script for the Podcast Index API integration.
This script will test your API key and secret by fetching a few podcasts.

Usage:
    python test_podcast_api.py [api_key] [api_secret]
    
If no API key/secret is provided, it will try to use the ones configured in Django settings or .env file.
"""

import os
import sys
import time
import hashlib
import requests
import json

def test_podcast_index_api(api_key, api_secret):
    """Test the Podcast Index API directly with REST calls"""
    print("Testing Podcast Index API connection with direct REST calls...")
    
    # Generate the authorization headers
    current_time = str(int(time.time()))
    api_header_hash = hashlib.sha1(f"{api_key}{api_secret}{current_time}".encode()).hexdigest()
    
    headers = {
        'X-Auth-Date': current_time,
        'X-Auth-Key': api_key,
        'Authorization': api_header_hash,
        'User-Agent': 'MindfulSpaceMentalHealthPlatform/1.0'
    }
    
    # Search for mental health podcasts
    search_url = "https://api.podcastindex.org/api/1.0/search/byterm?q=mental+health&max=5"
    
    try:
        print(f"Making API request to: {search_url}")
        print(f"Using headers: X-Auth-Key={api_key[:5]}..., Authorization={api_header_hash[:5]}...")
        
        response = requests.get(search_url, headers=headers)
        
        print(f"Response status code: {response.status_code}")
        
        if response.status_code != 200:
            print(f"Response text: {response.text}")
        
        response.raise_for_status()  # Raise an exception for 4XX/5XX responses
        
        data = response.json()
        
        if 'status' in data and data['status'] == 'true':
            print("Connection successful!")
            print(f"Found {data['count']} podcasts")
            
            if 'feeds' in data and data['feeds']:
                print("\nTop 3 Mental Health Podcasts:")
                for i, podcast in enumerate(data['feeds'][:3], 1):
                    print(f"{i}. {podcast['title']} by {podcast.get('author', 'Unknown')}")
            
            return True
        else:
            print(f"Error: API returned status {data.get('status', 'unknown')}")
            print(f"Error description: {data.get('description', 'No error description provided')}")
            return False
    
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Podcast Index API: {str(e)}")
        return False

def read_env_file():
    """Read API key and secret from .env file"""
    api_key = None
    api_secret = None
    
    try:
        if os.path.exists('.env'):
            print("Loading credentials from .env file...")
            with open('.env', 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('#') or '=' not in line:
                        continue
                        
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # Remove quotes if present
                    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
                        value = value[1:-1]
                    
                    # Remove any trailing/leading whitespace again after removing quotes
                    value = value.strip()
                    
                    if key == 'PODCAST_INDEX_API_KEY':
                        api_key = value
                        print(f"Found API key: {value} (showing full key for debugging)")
                    elif key == 'PODCAST_INDEX_API_SECRET':
                        api_secret = value
                        print(f"Found API secret: {value} (showing full secret for debugging)")
            
            if not api_key or not api_secret:
                print("Warning: Podcast Index API credentials not found in .env file.")
    except Exception as e:
        print(f"Error reading .env file: {str(e)}")
    
    return api_key, api_secret

def main():
    """Main function to run API tests"""
    # Check for command line arguments
    if len(sys.argv) >= 3:
        api_key = sys.argv[1]
        api_secret = sys.argv[2]
        print(f"Using API key from command line: {api_key[:5]}...")
    else:
        # Try to get API keys from .env file
        api_key, api_secret = read_env_file()
        
        if api_key and api_secret:
            print(f"Using API key from .env file: {api_key[:5]}...")
        else:
            try:
                # Try to get from Django settings as a fallback
                import django
                from django.conf import settings
                
                if not os.environ.get('DJANGO_SETTINGS_MODULE'):
                    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mental_health_core.settings')
                    django.setup()
                
                if hasattr(settings, 'PODCAST_INDEX_API'):
                    api_key = settings.PODCAST_INDEX_API.get('API_KEY')
                    api_secret = settings.PODCAST_INDEX_API.get('API_SECRET')
                    
                    if api_key and api_secret:
                        print(f"Using API key from Django settings: {api_key[:5]}...")
                    else:
                        print("API key and/or secret not found in settings.PODCAST_INDEX_API")
                        print("Please provide them as command line arguments:")
                        print("  python test_podcast_api.py <api_key> <api_secret>")
                        return False
                else:
                    print("PODCAST_INDEX_API not configured in Django settings.")
                    print("Please provide API key and secret as command line arguments:")
                    print("  python test_podcast_api.py <api_key> <api_secret>")
                    return False
            except Exception as e:
                print(f"Error loading Django settings: {str(e)}")
                print("Please provide API key and secret as command line arguments:")
                print("  python test_podcast_api.py <api_key> <api_secret>")
                return False
    
    # Test the direct API connection
    if not api_key or not api_secret or api_key == 'your-api-key-here' or api_secret == 'your-api-secret-here':
        print("Error: Please provide valid API key and secret.")
        print("You are using placeholder values. Update with your actual Podcast Index API credentials.")
        return False
    
    if test_podcast_index_api(api_key, api_secret):
        print("\n✅ Direct API test successful!")
        return True
    else:
        print("\n❌ Direct API test failed.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

# Test with Django PodcastService
def test_podcast_service():
    """Test the Django PodcastService implementation"""
    try:
        # Set up Django environment
        import django
        from django.conf import settings
        
        # Check if we're already in a Django environment
        if not os.environ.get('DJANGO_SETTINGS_MODULE'):
            sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mental_health_core.settings')
            django.setup()
        
        # Import the podcast service
        try:
            from mental_health.services.podcast_service import PodcastService
            
            print("\nTesting PodcastService implementation...")
            service = PodcastService()
            
            # Test search
            print("\nSearching for 'mental health' podcasts:")
            podcasts = service.search_podcasts("mental health", max_results=3)
            
            if podcasts:
                print(f"Found {len(podcasts)} podcasts")
                for i, podcast in enumerate(podcasts, 1):
                    print(f"{i}. {podcast['title']} by {podcast['author']}")
                
                # Test episodes
                if podcasts:
                    podcast_id = podcasts[0]['id']
                    print(f"\nFetching episodes for '{podcasts[0]['title']}':")
                    episodes = service.get_podcast_episodes(podcast_id, max_results=3)
                    
                    if episodes:
                        print(f"Found {len(episodes)} episodes")
                        for i, episode in enumerate(episodes, 1):
                            print(f"{i}. {episode['title']} ({episode['duration']} mins)")
                    else:
                        print("No episodes found.")
                
                return True
            else:
                print("No podcasts found.")
                return False
            
        except ImportError:
            print("PodcastService not found. Skipping Django service test.")
            return None
    
    except Exception as e:
        print(f"Error testing Django PodcastService: {str(e)}")
        return False

def main():
    """Main function to run all tests"""
    # Check for command line arguments
    if len(sys.argv) >= 3:
        api_key = sys.argv[1]
        api_secret = sys.argv[2]
        print(f"Using API key from command line: {api_key[:5]}...")
        
        # Test with direct API calls
        if test_podcast_index_api(api_key, api_secret):
            print("\n✅ Direct API test successful!")
        else:
            print("\n❌ Direct API test failed.")
            return False
    else:
        # Try to get API keys from Django settings
        try:
            import django
            from django.conf import settings
            
            if not os.environ.get('DJANGO_SETTINGS_MODULE'):
                sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mental_health_core.settings')
                django.setup()
            
            if hasattr(settings, 'PODCAST_INDEX_API'):
                api_key = settings.PODCAST_INDEX_API.get('API_KEY')
                api_secret = settings.PODCAST_INDEX_API.get('API_SECRET')
                
                if api_key and api_secret:
                    print(f"Using API key from Django settings: {api_key[:5]}...")
                    
                    # Test with direct API calls
                    if test_podcast_index_api(api_key, api_secret):
                        print("\n✅ Direct API test successful!")
                    else:
                        print("\n❌ Direct API test failed.")
                        return False
                else:
                    print("API key and/or secret not found in settings.PODCAST_INDEX_API")
                    print("Please provide them as command line arguments:")
                    print("  python test_podcast_api.py <api_key> <api_secret>")
                    return False
            else:
                print("PODCAST_INDEX_API not configured in Django settings.")
                print("Please provide API key and secret as command line arguments:")
                print("  python test_podcast_api.py <api_key> <api_secret>")
                return False
        except Exception as e:
            print(f"Error loading Django settings: {str(e)}")
            print("Please provide API key and secret as command line arguments:")
            print("  python test_podcast_api.py <api_key> <api_secret>")
            return False
    
    # Test the Django service implementation
    service_result = test_podcast_service()
    if service_result is True:
        print("\n✅ Django PodcastService test successful!")
    elif service_result is False:
        print("\n❌ Django PodcastService test failed.")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

def main():
    """Main function"""
    # Try to load API key and secret from .env file or environment variables
    try:
        # Check if .env file exists
        if os.path.exists('.env'):
            print("Loading credentials from .env file...")
            with open('.env', 'r') as f:
                for line in f:
                    if '=' in line:
                        key, value = line.strip().split('=', 1)
                        os.environ[key] = value
        
        api_key = os.environ.get('PODCAST_INDEX_API_KEY')
        api_secret = os.environ.get('PODCAST_INDEX_API_SECRET')
        
        if not api_key or not api_secret:
            print("API key or secret not found.")
            api_key = input("Enter your Podcast Index API Key: ")
            api_secret = input("Enter your Podcast Index API Secret: ")
        
        success = test_podcast_index_api(api_key, api_secret)
        
        if success:
            print("\nYour Podcast Index API is working correctly!")
            print("You can now use the podcast features in your mental health platform.")
        else:
            print("\nFailed to connect to the Podcast Index API.")
            print("Please check your API key and secret.")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
