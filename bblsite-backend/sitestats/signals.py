import datetime

from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.utils import timezone

from sitestats.models import SiteStat
from siteusers.models import Player


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    try:
        player = Player.objects.get(site_user=user)
    except Player.DoesNotExist:
        pass
    else:
        SiteStat.objects.create(
            player=player,
            event=SiteStat.Event.LOGIN,
            timestamp=timezone.now()
        )


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    try:
        player = Player.objects.get(site_user=user)
    except Player.DoesNotExist:
        pass
    else:
        logout_event = SiteStat.objects.create(
            player=player,
            event=SiteStat.Event.LOGOUT,
            timestamp=timezone.now()
        )
        last_login_event = SiteStat.objects.filter(player=player, event=SiteStat.Event.LOGIN).order_by('-timestamp').first()
        time_diff = logout_event.timestamp - last_login_event.timestamp
        player.total_time += int(time_diff.total_seconds())
        player.save()