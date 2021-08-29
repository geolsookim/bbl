import random

from faker import Faker

from django.core.management.base import BaseCommand
from rest_framework.authtoken.models import Token

from siteusers.models import SiteUser, Player
from league.models import Team


class Command(BaseCommand):
    help = "Initialise site users and players."

    def create_site_user(self):
        faker = Faker()
        created = False
        while not created:
            first_name = faker.first_name()
            last_name = faker.last_name()
            username = first_name.lower() + '.' + last_name.lower()
            site_user, created = SiteUser.objects.get_or_create(
                username=username,
                email=f'{username}@bbl.com',
                first_name=first_name,
                last_name=last_name,
            )
            if not created:
                continue
            site_user.set_password('password')
            site_user.save()
            Token.objects.get_or_create(user=site_user)
        return site_user

    def handle(self, *args, **options):
        # create site admin
        admin = SiteUser.objects.create(
            username='admin',
            email='admin@bbl.com'
        )
        admin.set_password('password')
        admin.is_staff = True
        admin.is_superuser = True
        admin.save()

        # create league admin
        league_admin = self.create_site_user()
        league_admin.is_league_admin = True
        league_admin.save()

        faker = Faker()
        # create coaches
        for i in range(16):
            coach = self.create_site_user()
            coach.is_coach = True
            coach.save()
            team_name = faker.user_name()
            Team.objects.create(coach=coach, name=team_name)

        # create players
        teams = Team.objects.all()
        for i in range(16):
            for j in range(10):
                player = self.create_site_user()
                player.is_player = True
                player.save()
                height = random.randrange(190, 230)
                Player.objects.create(site_user=player, height=height, team=teams[i])


