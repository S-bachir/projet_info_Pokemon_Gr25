from PyInquirer import prompt, Separator

from view.abstract_vue import AbstractView
from time_print import delay_print


class PokedexView(AbstractView):

    def __init__(self):

        self.questions = [
            {
                'type': 'list',
                'name': 'choix_menu',
                'message': 'Menu : Veuillez choisir un menu',
                'choices': [
                    "Consulter les pokémons rencontrés",
                    "Consulter les pokémons capturés",
                    Separator(),
                    "Retour au menu principal"
                ]
            }
        ]

    def display_info(self):
        print("\t***************",
              "\n\t*   Pokédex   *",
              "\n\t***************\n")

    def make_choice(self):

        reponse = prompt(self.questions)

        if reponse["choix_menu"] == "Consulter les pokémons rencontrés":
            from view.poke_rencont_view import PokeRencontreView
            next_view = PokeRencontreView()

        elif reponse["choix_menu"] == "Consulter les pokémons capturés":
            from view.poke_capture_view import PokeCaptureView
            next_view = PokeCaptureView()

        else:
            from view.menu_principal_view import MenuPrincipalView
            next_view = MenuPrincipalView()

        return next_view
