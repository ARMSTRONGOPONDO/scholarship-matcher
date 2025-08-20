"""
This file is needed to make the views package importable.
"""

from .base_views import (
    index,
    CategoryViewSet,
    ResourceViewSet,
    DisorderViewSet,
    TherapistViewSet,
    CrisisResourceViewSet,
    StatisticViewSet
)

from .auth_views import (
    RegisterView,
    LoginView,
    UserProfileView,
    subscribe_newsletter,
    save_resource
)

from .search_views import search
from .podcast_views import PodcastViewSet, search_podcasts, get_podcast_episodes

__all__ = [
    'index',
    'CategoryViewSet',
    'ResourceViewSet',
    'DisorderViewSet',
    'TherapistViewSet',
    'CrisisResourceViewSet',
    'StatisticViewSet',
    'RegisterView',
    'LoginView',
    'UserProfileView',
    'subscribe_newsletter',
    'save_resource',
    'search',
    'PodcastViewSet',
    'search_podcasts',
    'get_podcast_episodes'
]

from mental_health.views import (
    CategoryViewSet, ResourceViewSet, DisorderViewSet,
    TherapistViewSet, CrisisResourceViewSet, StatisticViewSet,
    RegisterView, LoginView, UserProfileView,
    subscribe_newsletter, save_resource, search, index
)

from .podcast_views import PodcastViewSet, search_podcasts, get_podcast_episodes

__all__ = [
    'CategoryViewSet',
    'ResourceViewSet',
    'DisorderViewSet',
    'TherapistViewSet',
    'CrisisResourceViewSet',
    'StatisticViewSet',
    'PodcastViewSet',
    'RegisterView',
    'LoginView',
    'UserProfileView',
    'subscribe_newsletter',
    'save_resource',
    'search',
    'search_podcasts',
    'get_podcast_episodes',
    'index'
]
