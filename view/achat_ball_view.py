from PyInquirer import prompt, Separator

from service.magasin_service import MagasinService
from service.ball_service import BallService
from service.dresseur_service import DresseurService
from view.abstract_vue import AbstractView
import pandas as pd

from time_print import delay_print


class AchatBallView(AbstractView):

    def __init__(self):
        # la liste des balls que l'on affiche
        self.balls_objects = \
            MagasinService.get_all_balls_from_db()
        # la liste avec uniquement les noms
        self.ball_nom = [ball.name_ball for ball in
                         self.balls_objects]

        # Création du menu
        choix_ball = self.ball_nom
        choix_ball.append(Separator())
        choix_ball.append("Retour menu principal")
        self.questions = [
            {
                'type': 'list',
                'name': 'choix_menu',
                'message': 'Menu : Veillez choisir le ball à acheter',
                'choices': choix_ball
            }
        ]

    def display_info(self):
        print("\t****************",
              "\n\t*   Boutique   *",
              "\n\t****************\n")
        delay_print("Nom du dresseur : {}\n".format(
            AbstractView.session.dresseur_actif.nom_dresseur))
        delay_print("Son identifiant : {}\n".format(
            AbstractView.session.dresseur_actif.id_dresseur))
        delay_print("Son argent: {}\n".format(
            AbstractView.session.dresseur_actif.argent))

    def make_choice(self):
        ball_prix = [ball.prix for ball in self.balls_objects]
        ball_nom = [ball.name_ball for ball in self.balls_objects]
        df = pd.DataFrame({"Ball": ball_nom, "prix": ball_prix})
        print("\n============================================\n")
        print(df)
        print("\n============================================\n")

        reponse = prompt(self.questions)
        if reponse["choix_menu"] == "Retour menu principal":
            from view.menu_principal_view import MenuPrincipalView
            next_view = MenuPrincipalView()
        else:
            index = self.ball_nom.index(reponse["choix_menu"])
            ball_choisi = self.balls_objects[index]
            achat = MagasinService.acheter_ball(
                AbstractView.session.dresseur_actif, ball_choisi)

            liste_balls = BallService.get_all_balls_from_db(
                AbstractView.session.dresseur_actif.id_dresseur
            )

            if achat is True and reponse["choix_menu"] not in liste_balls:
                delay_print("\nBall acheté!")
                AbstractView.session.dresseur_actif.argent = \
                    AbstractView.session.dresseur_actif.argent - ball_choisi.prix
                DresseurService.update_dresseur_in_db(
                    AbstractView.session.dresseur_actif
                )
                BallService.add_ball_in_db(
                    AbstractView.session.dresseur_actif, ball_choisi)

            elif achat is False:
                delay_print("\nvous ne disposer pas assez d'argent pour acheter ce ball")

            else:
                delay_print("\nCe ball existe déjà dans votre base de donnée.")
                delay_print("\n\nveuillez l'utiliser avant d'acheter un autre.")

            next_view = AchatBallView()

        return next_view
