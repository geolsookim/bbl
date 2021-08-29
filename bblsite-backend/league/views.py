from .models import Team, Game
from rest_framework import viewsets
from rest_framework import permissions
from .serialisers import TeamSerialiser, GameSerialiser

from siteusers.permissions import IsTeamCoachOrPlayer


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerialiser
    permission_classes = [permissions.IsAuthenticated, IsTeamCoachOrPlayer]


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerialiser
    permission_classes = [permissions.IsAuthenticated]
