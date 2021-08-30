from rest_framework.permissions import BasePermission


class IsLeagueAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_league_admin