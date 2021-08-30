from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from league.views import TeamViewSet, GameViewSet
from siteusers.views import PlayerViewSet
from sitestats.views import site_stats

router = routers.DefaultRouter()
router.register(r'api/v1/team', TeamViewSet)
router.register(r'api/v1/game', GameViewSet)
router.register(r'api/v1/player', PlayerViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/v1/dj-rest-auth/', include('dj_rest_auth.urls')),
    path('api/v1/site_stats', site_stats, name='site_stats'),
]