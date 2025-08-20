from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.views import APIView

from ..services.podcast_service import PodcastService

class PodcastViewSet(APIView):
    """
    API view for retrieving mental health podcasts from Podcast Index
    """
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, format=None):
        """
        Get mental health podcasts
        """
        podcast_service = PodcastService()
        category = request.query_params.get('category', 'popular')
        max_results = int(request.query_params.get('max_results', 10))
        
        try:
            podcasts = podcast_service.get_mental_health_podcasts(category, max_results)
            return Response(podcasts)
        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": f"Error retrieving podcasts: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def search_podcasts(request):
    """
    Search for mental health podcasts
    """
    query = request.query_params.get('q', '')
    max_results = int(request.query_params.get('max_results', 10))
    
    if not query:
        return Response(
            {"error": "Query parameter 'q' is required"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    podcast_service = PodcastService()
    podcasts = podcast_service.search_podcasts(query, max_results)
    return Response(podcasts)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_podcast_episodes(request, podcast_id):
    """
    Get episodes for a specific podcast
    """
    max_results = int(request.query_params.get('max_results', 10))
    
    podcast_service = PodcastService()
    episodes = podcast_service.get_podcast_episodes(podcast_id, max_results)
    return Response(episodes)
