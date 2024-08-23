from PyInquirer import prompt, Separator

from service.pokedex_service import PokedexService
from view.abstract_vue import AbstractView
from service.ball_service import BallService
from service.capture_poke_service import CapturePokeService
from metier.pokedex import Pokedex
import time

from time_print import delay_print


class CapturePokeView(AbstractView):

    def __init__(self, objet_poke_adverse):
        self.objet_poke_adverse = objet_poke_adverse

        self.questions = [
            {
                'type': 'list',
                'name': 'choix_menu',
                'message': 'Menu : Voulez vous capturer le pokemon adverse',
                'choices': ["oui", "non"]
            }
        ]

        # la liste des balls que l'on affiche
        self.ball_nom = BallService.get_all_balls_from_db(
                AbstractView.session.dresseur_actif.id_dresseur
            )

        # Création du menu
        choix_ball = self.ball_nom
        choix_ball.append(Separator())
        choix_ball.append("Retour au menu principal")

        self.questions_ball = [
            {
                'type': 'list',
                'name': 'choix_menu',
                'message': 'Menu : Quel ball voulez vous utiliser?',
                'choices': choix_ball
            }
        ]

    def display_info(self):
        print("Nom du dresseur actif : {}".format(AbstractView.session.dresseur_actif.nom_dresseur))
        print("Son identifiant : {}".format(
            AbstractView.session.dresseur_actif.id_dresseur))
        print("Son argent: {}".format(
            AbstractView.session.dresseur_actif.argent))
        print("Le pokemon actif : {}\n".format(
            AbstractView.session.dresseur_actif.pokemon_actif))

    def make_choice(self):

        reponse1 = prompt(self.questions)
        if reponse1["choix_menu"] == "non":
            pass
        else:
            reponse2 = prompt(self.questions_ball)

            if reponse2["choix_menu"] == "Retour au menu principal":
                pass
            else:
                delay_print("\n{} utilise {} pour capturer le pokemon adverse".format(
                    AbstractView.session.pokemon_actif.nom_poke,
                    reponse2["choix_menu"]
                ))

                # c'est ici qu'il faut capturer le pokemon adverse
                capture = CapturePokeService.capture_pokemon(
                    self.objet_poke_adverse, reponse2["choix_menu"]
                )
                if capture is False:
                    time.sleep(2)
                    delay_print("\nEchec! Le pokémon n'a pas été capturé!")

                else:
                    time.sleep(2)
                    delay_print("\nSuccès! Le pokémon est capturé et stocké dans le pokédex!")
                    # ajouter le pokemon dans le pokedex
                    objet_dresseur = AbstractView.session.dresseur_actif

                    if (objet_dresseur.id_dresseur, "C") not in PokedexService.get_all_pokedex():
                        PokedexService.add_pokemon_to_pokedex(
                            AbstractView.session.dresseur_actif, Pokedex(), "C"
                        )

                    pokedex_c = PokedexService.get_all_pokemons_c(objet_dresseur)
                    PokedexService.update_pokemon_in_pokedex(
                        pokedex_c, self.objet_poke_adverse
                    )

                BallService.delete_ball_from_db(
                    AbstractView.session.dresseur_actif
                )

        from view.menu_principal_view import MenuPrincipalView
        next_view = MenuPrincipalView()
        return next_view
