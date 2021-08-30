from django.contrib import admin

from .models import SiteUser, Player


class SiteUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_player', 'is_coach', 'is_league_admin')


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'height', 'get_team')
    fields = ['get_name', 'height', 'get_team', 'average_score', 'games_played', 'total_time']
    readonly_fields = ['get_name', 'get_team', 'average_score', 'games_played', 'total_time']

    @admin.display(description='Name', ordering='siteusers__name')
    def get_name(self, obj):
        return f"{obj.site_user.first_name} {obj.site_user.last_name}"

    @admin.display(description='Team', ordering='team__name')
    def get_team(self, obj):
        return obj.team.name


admin.site.register(SiteUser, SiteUserAdmin)
admin.site.register(Player, PlayerAdmin)
