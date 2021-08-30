import json

from django.shortcuts import render
from django.db.models import Count
from django.utils import timezone

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import SiteStat
from .permissions import IsLeagueAdmin
from siteusers.models import Player


def get_current_logins():
    # this function will need to be optimised in a subsequent iteration
    current_logins = []
    for player in Player.objects.all():
        last_login = SiteStat.objects.filter(player=player, event=SiteStat.Event.LOGIN).order_by('-timestamp').first()
        if not last_login:
            continue
        last_logout = SiteStat.objects.filter(player=player, event=SiteStat.Event.LOGOUT).order_by('-timestamp').first()
        if not last_logout or last_logout.timestamp < last_login.timestamp:
            current_logins.append(player.site_user.username)
        return current_logins


@api_view(['GET'])
@permission_classes([IsLeagueAdmin,])
def site_stats(request, **kwargs):
    player_logins = list(Player.objects.filter(player_site_stats__event='login')
                         .annotate(num_logins=Count('player_site_stats'))
                         .values('site_user__username', 'num_logins'))
    player_total_time_spent = list(Player.objects.values('site_user__username', 'total_time'))
    current_logins = get_current_logins()

    return Response({
        'player_logins': player_logins,
        'player_total_time_spent': player_total_time_spent,
        'current_logins': current_logins,
    })
