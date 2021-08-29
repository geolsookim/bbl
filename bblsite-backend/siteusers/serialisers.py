from rest_framework import serializers

from .models import Player


class PlayerSerialiser(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    team = serializers.SerializerMethodField()

    class Meta:
        model = Player
        fields = ['id', 'full_name', 'height', 'team', 'average_score', 'games_played']

    def get_full_name(self, player):
        return player.site_user.get_full_name()

    def get_team(self, player):
        return player.team.name.title()

    def get_average_score(self, player):
        return player.average_score

    def get_games_played(self, player):
        return player.games_played
