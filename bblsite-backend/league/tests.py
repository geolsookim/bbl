from django.core.management import call_command
from django.test import TestCase, RequestFactory
from rest_framework.test import force_authenticate
from rest_framework import status

from siteusers.models import SiteUser, Player
from league.models import Team, Game, PlayerGame
from league.views import TeamViewSet


class StatTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        call_command('init_site_users')
        call_command('init_league')

    def setUp(self):
        self.player = Player.objects.first()
        self.team = Team.objects.first()
        self.game = Game.objects.first()

    def test_player_average_score(self):
        game_scores = [game.score for game in PlayerGame.objects.filter(player=self.player)]
        average_score = round(sum(game_scores)/len(game_scores), 2) if game_scores else 0
        self.assertEqual(average_score, self.player.average_score)

    def test_player_games_played(self):
        games_played = PlayerGame.objects.filter(player=self.player).count()
        self.assertEqual(games_played, self.player.games_played)

    def test_team_average_score(self):
        home_game_scores = [game.home_team_score for game in Game.objects.filter(home_team=self.team)]
        away_game_scores = [game.away_team_score for game in Game.objects.filter(away_team=self.team)]
        combined_scores = home_game_scores + away_game_scores
        average_score = round(sum(combined_scores)/len(combined_scores), 2)
        self.assertEqual(average_score, self.team.average_score)

    def test_game_home_team_score(self):
        team_members = self.game.players.filter(team=self.game.home_team)
        game_players = PlayerGame.objects.filter(player__in=team_members, game=self.game)
        score = sum(list(game_players.values_list('score', flat=True)))
        self.assertEqual(score, self.game.home_team_score)

    def test_game_away_team_score(self):
        team_members = self.game.players.filter(team=self.game.away_team)
        game_players = PlayerGame.objects.filter(player__in=team_members, game=self.game)
        score = sum(list(game_players.values_list('score', flat=True)))
        self.assertEqual(score, self.game.away_team_score)

    def test_game_winner(self):
        winner = self.game.home_team if self.game.home_team_score > self.game.away_team_score else self.game.away_team
        self.assertEqual(winner, self.game.winner)


class TeamViewsetTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        call_command('init_site_users')
        call_command('init_league')

    def setUp(self):
        self.factory = RequestFactory()
        self.coach = SiteUser.objects.filter(is_coach=True).first()
        self.coach_team = self.coach.team_set.all().first()
        self.other_team = Team.objects.exclude(coach=self.coach).first()

    def test_coach_can_view_own_team(self):
        request = self.factory.get(f'/api/v1/team/{self.coach_team.id}/')
        force_authenticate(request, user=self.coach)
        view = TeamViewSet.as_view({'get': 'retrieve'})
        response = view(request, pk=self.coach_team.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.status_text, 'OK')
        self.assertEqual(response.data.get('name').lower(), self.coach_team.name.lower())

    def test_coach_cant_view_other_team(self):
        request = self.factory.get(f'/api/v1/team/{self.other_team.id}/')
        force_authenticate(request, user=self.coach)
        view = TeamViewSet.as_view({'get': 'retrieve'})
        response = view(request, pk=self.other_team.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_text, 'Forbidden')
        error_detail = response.data.get('detail')
        self.assertEqual(str(error_detail), 'You do not have permission to perform this action.')
