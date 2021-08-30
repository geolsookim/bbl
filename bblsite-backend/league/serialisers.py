from rest_framework import serializers

from league.models import Team, Game
from siteusers.serialisers import PlayerSerialiser


class TeamSerialiser(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    coach = serializers.SerializerMethodField()
    average_score = serializers.SerializerMethodField()
    ninetieth_percentile = serializers.SerializerMethodField
    members = PlayerSerialiser(source='player_set', many=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'coach', 'average_score', 'ninetieth_percentile', 'members']

    def get_name(self, team):
        return team.name.title()

    def get_coach(self, team):
        return team.coach.get_full_name()

    def get_average_score(self, team):
        return team.average_score

    def get_ninetieth_percentile(self, team):
        return team.ninetieth_percentile


class GameSerialiser(serializers.ModelSerializer):
    round = serializers.SerializerMethodField()
    home_team_id = serializers.SerializerMethodField()
    home_team = serializers.SerializerMethodField()
    home_team_score = serializers.SerializerMethodField()
    away_team_id = serializers.SerializerMethodField()
    away_team = serializers.SerializerMethodField()
    away_team_score = serializers.SerializerMethodField()
    winner = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = ['id', 'round', 'home_team_id', 'home_team', 'home_team_score', 'away_team_id', 'away_team', 'away_team_score', 'winner']

    def get_round(self, game):
        return Game.Round(game.round).label

    def get_home_team_id(self, game):
        return game.home_team.id

    def get_home_team(self, game):
        return game.home_team.name

    def get_home_team_score(self, game):
        return game.home_team_score

    def get_away_team_id(self, game):
        return game.away_team.id

    def get_away_team(self, game):
        return game.away_team.name

    def get_away_team_score(self, game):
        return game.away_team_score

    def get_winner(self, game):
        return game.winner.name