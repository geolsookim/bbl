from django.core.management import call_command
from django.test import TestCase, RequestFactory
from rest_framework.test import force_authenticate
from rest_framework import status

from siteusers.models import SiteUser, Player
from siteusers.views import PlayerViewSet
from league.models import Team


class InitSiteUsersTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        call_command('init_site_users')

    def test_site_users_count(self):
        self.assertEqual(SiteUser.objects.count(), 178)

    def test_player_count(self):
        self.assertEqual(Player.objects.count(), 160)

    def test_coach_count(self):
        self.assertEqual(SiteUser.objects.filter(is_coach=True).count(), 16)

    def test_team_count(self):
        self.assertEqual(Team.objects.count(), 16)


class PlayerViewsetTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        call_command('init_site_users')

    def setUp(self):
        self.factory = RequestFactory()
        self.coach = SiteUser.objects.filter(is_coach=True).first()
        self.coach_team = self.coach.team_set.all().first()
        self.coached_player = Player.objects.filter(team=self.coach_team).first()
        self.other_team_player = Player.objects.exclude(team=self.coach_team).first()

    def test_coach_can_view_own_player(self):
        request = self.factory.get(f'/api/v1/player/{self.coached_player.id}/')
        force_authenticate(request, user=self.coach)
        view = PlayerViewSet.as_view({'get': 'retrieve'})
        response = view(request, pk=self.coached_player.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.status_text, 'OK')
        self.assertEqual(response.data.get('full_name'), self.coached_player.site_user.get_full_name())

    def test_coach_cant_view_other_team_player(self):
        request = self.factory.get(f'/api/v1/player/{self.other_team_player.id}/')
        force_authenticate(request, user=self.coach)
        view = PlayerViewSet.as_view({'get': 'retrieve'})
        response = view(request, pk=self.other_team_player.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_text, 'Forbidden')
        error_detail = response.data.get('detail')
        self.assertEqual(str(error_detail), 'You do not have permission to perform this action.')

