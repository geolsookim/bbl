import random

from django.core.management.base import BaseCommand

from league.models import Game, Team, PlayerGame


class Command(BaseCommand):
    help = "Initialise league."

    def create_game(self, home_team, away_team, round):
        game = Game.objects.create(
            round=round,
            home_team=home_team,
            away_team=away_team,
        )
        # "not all players participate in every game"
        home_team_members = random.sample(list(home_team.player_set.all()), 7)
        for player in home_team_members:
            score = random.randrange(0, 40)
            PlayerGame.objects.create(player=player, game=game, score=score)
        away_team_members = random.sample(list(away_team.player_set.all()), 7)
        for player in away_team_members:
            score = random.randrange(0, 30)
            PlayerGame.objects.create(player=player, game=game, score=score)

    def handle(self, *args, **options):
        # sweet sixteen
        teams = Team.objects.all()
        for i in range(0, 16, 2):
            self.create_game(home_team=teams[i], away_team=teams[i+1], round=Game.Round.SWEET_SIXTEEN)

        # quarter finals
        quarter_final = [game.winner for game in Game.objects.filter(round=Game.Round.SWEET_SIXTEEN)]
        for i in range(0, 8, 2):
            self.create_game(home_team=quarter_final[i], away_team=quarter_final[i+1], round=Game.Round.QUARTER_FINAL)

        # semi finals
        semi_final = [game.winner for game in Game.objects.filter(round=Game.Round.QUARTER_FINAL)]
        for i in range(0, 4, 2):
            self.create_game(home_team=semi_final[i], away_team=semi_final[i+1], round=Game.Round.SEMI_FINAL)

        # final
        final = [game.winner for game in Game.objects.filter(round=Game.Round.SEMI_FINAL)]
        self.create_game(home_team=final[0], away_team=final[1], round=Game.Round.FINAL)