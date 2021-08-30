from django.contrib import admin

from .models import SiteStat


class SiteStatAdmin(admin.ModelAdmin):
    list_display = ('player', 'event', 'timestamp')


admin.site.register(SiteStat, SiteStatAdmin)
