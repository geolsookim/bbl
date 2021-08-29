from rest_framework.permissions import BasePermission

class IsTeamCoachOrPlayer(BasePermission):

    def has_object_permission(self, request, view, obj):
        if any([request.user.is_league_admin,
                request.user.is_superuser,
                (request.user.is_coach and obj == request.user.team_set.first()),
                (request.user.is_player and request.user.player.team == obj)
                ]):
            return True
        else:
            return False

class IsCoachOrPlayer(BasePermission):

    def has_object_permission(self, request, view, obj):
        if any([request.user.is_league_admin,
                request.user.is_superuser,
                (request.user.is_coach and obj.team == request.user.team_set.first()),
                (request.user.is_player and request.user.player == obj)
                ]):
            return True
        else:
            return False
