import json

from django.shortcuts import render
from django.db.models import Count

from rest_framework.decorators import api_view, permission_classes

from .models import SiteStat
from siteusers.models import Player


@api_view(['GET'])
@permission_classes((AllowAny,))
def site_stats(request, client, **kwargs):
    player_logins = list(Player.objects.annotate(num_logins=Count('player_site_stats')).values('site_user__username', 'num_logins'))

    return Response({
        'player_logins': player_logins,
    })
