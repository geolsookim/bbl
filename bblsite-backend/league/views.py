from .models import Team, Game

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from .serialisers import TeamSerialiser, GameSerialiser
from siteusers.serialisers import PlayerSerialiser

from siteusers.permissions import IsTeamCoachOrPlayer


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerialiser
    permission_classes = [permissions.IsAuthenticated, IsTeamCoachOrPlayer]

    @action(detail=True)
    def ninetieth(self, request, pk=None):
        team = self.get_object()
        serializer = PlayerSerialiser(team.ninetieth_percentile_players, many=True)
        return Response(serializer.data)


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerialiser
    permission_classes = [permissions.IsAuthenticated]