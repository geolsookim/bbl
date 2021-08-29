from django.db import models
from django.contrib.auth.models import AbstractUser


class SiteUser(AbstractUser):
    is_player = models.BooleanField('is a player', default=False)
    is_coach = models.BooleanField('is a coach', default=False)
    is_league_admin = models.BooleanField('is a league admin', default=False)

    class Meta:
        verbose_name = 'Site User'

    def __str__(self):
        return str(self.username)


class Player(models.Model):
    site_user = models.OneToOneField(SiteUser, on_delete=models.CASCADE)
    height = models.IntegerField(help_text="Height in centimetres", default=0)
    team = models.ForeignKey('league.Team', on_delete=models.CASCADE)
    game = models.ManyToManyField('league.Game', through='league.PlayerGame', blank=True, related_name='players')

    @property
    def average_score(self):
        from league.models import PlayerGame
        game_scores = [game.score for game in PlayerGame.objects.filter(player=self)]
        return round(sum(game_scores)/len(game_scores), 2) if game_scores else 0

    @property
    def games_played(self):
        from league.models import PlayerGame
        return PlayerGame.objects.filter(player=self).count()

    def __str__(self):
        return str(self.site_user.username)

