from django.contrib import admin

from .models import Team, Game, PlayerGame
from siteusers.models import Player


class PlayerInline(admin.TabularInline):
    model = Player


class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'coach')
    fields = ['name', 'coach', 'average_score']
    readonly_fields = ['average_score',]
    inlines = [PlayerInline]


class GameAdmin(admin.ModelAdmin):
    list_display = ('round', 'home_team', 'home_team_score', 'away_team', 'away_team_score')
    readonly_fields = ['round', 'home_team', 'home_team_score', 'away_team', 'away_team_score', 'winner']


class PlayerGameAdmin(admin.ModelAdmin):
    list_display = ('player', 'game', 'score')


admin.site.register(Team, TeamAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(PlayerGame, PlayerGameAdmin)
