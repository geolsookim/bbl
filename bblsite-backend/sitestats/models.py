import datetime

from django.conf import settings
from django.db import models
from django.utils import timezone

from siteusers.models import Player

class SiteStat(models.Model):
    class Event(models.TextChoices):
        LOGIN = 'login', 'Login'
        LOGOUT = 'logout', 'Logout'

    player = models.ForeignKey(Player, related_name="player_site_stats", on_delete=models.CASCADE)
    event = models.CharField(max_length=10, choices=Event.choices)
    timestamp = models.DateTimeField(
        help_text="The time at which the first visit of the day was recorded",
        default=timezone.now,
    )

    def __str__(self):
        return str(self.player.site_user.username)

