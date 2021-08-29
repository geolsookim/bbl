from django.shortcuts import render

from .models import Player
from rest_framework import viewsets
from rest_framework import permissions
from .serialisers import PlayerSerialiser
from .permissions import IsCoachOrPlayer


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerialiser
    permission_classes = [permissions.IsAuthenticated, IsCoachOrPlayer]