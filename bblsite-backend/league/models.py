import math

from django.db import models

from siteusers.models import SiteUser, Player


class Team(models.Model):
    name = models.CharField(max_length=255)
    coach = models.ForeignKey(SiteUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    @property
    def average_score(self) -> float:
        home_game_scores = [game.home_team_score for game in Game.objects.filter(home_team=self)]
        away_game_scores = [game.away_team_score for game in Game.objects.filter(away_team=self)]
        combined_scores = home_game_scores + away_game_scores
        return round(sum(combined_scores)/len(combined_scores), 2)

    @property
    def ninetieth_percentile(self) -> float:
        samples = sorted(player.average_score for player in self.player_set.all())
        ninetieth_percentile_index = math.ceil(0.9 * len(samples)) - 1
        return samples[ninetieth_percentile_index]

    @property
    def ninetieth_percentile_players(self) -> list:
        return [player for player in self.player_set.all() if player.average_score >= self.ninetieth_percentile]


class Game(models.Model):
    class Round(models.TextChoices):
        SWEET_SIXTEEN = 'ss', 'Sweet Sixteen'
        QUARTER_FINAL = 'qf', 'Quarter Final'
        SEMI_FINAL = 'sf', 'Semi Final'
        FINAL = 'fi', 'Final'

    round = models.CharField(max_length=2, choices=Round.choices, default=Round.SWEET_SIXTEEN)
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_team')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_team')

    def __str__(self):
        return f"{self.round} {self.home_team.name} v {self.away_team.name}"

    @property
    def home_team_score(self) -> int:
        team_members = self.players.filter(team=self.home_team)
        game_players = PlayerGame.objects.filter(player__in=team_members, game=self)
        return sum(list(game_players.values_list('score', flat=True)))

    @property
    def away_team_score(self) -> int:
        team_members = self.players.filter(team=self.away_team)
        game_players = PlayerGame.objects.filter(player__in=team_members, game=self)
        return sum(list(game_players.values_list('score', flat=True)))

    @property
    def winner(self) -> Team:
        return self.home_team if self.home_team_score > self.away_team_score else self.away_team


class PlayerGame(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_games')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='game_players')
    score = models.IntegerField()

    def __str__(self):
        return f"{self.player.site_user.username} {self.game} {self.score}"


