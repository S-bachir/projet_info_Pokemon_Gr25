from PyInquirer import prompt, Separator

from view.abstract_vue import AbstractView
from service.pokedex_service import PokedexService
from service.pokemon_service import PokemonService

from time_print import delay_print


class PokeRencontreView(AbstractView):

    def __init__(self):

        objet_dresseur = AbstractView.session.dresseur_actif
        self.pokedex = PokedexService.get_all_pokemons_r(
            objet_dresseur)

        if self.pokedex is None:
            pass
        else:
            self.liste = self.pokedex.liste_id_poke.split(',')
            liste_nom = [PokemonService.get_pokemon_from_db_by_id(i).nom_poke for i in self.liste[:-1]]
            liste_nom.sort()

            self.questions = [
                {
                    'type': 'list',
                    'name': 'choix_menu',
                    'message': 'Veillez choisir un pokemon :',
                    'choices': liste_nom + [Separator(), "Retour au menu principal"]
                }
            ]

    def display_info(self):
        pass

    def make_choice(self):

        if self.pokedex is None:

            delay_print("le pokédex est vide !\n")
            delay_print("vous n'avez pas encore rencontré des pokémons !\n")

            from view.menu_principal_view import MenuPrincipalView
            next_view = MenuPrincipalView()

        else:

            reponse = prompt(self.questions)

            if reponse["choix_menu"] == "Retour au menu principal":
                from view.menu_principal_view import MenuPrincipalView
                next_view = MenuPrincipalView()

            else:
                from view.stat_poke_view import StatPokeView
                next_view = StatPokeView(reponse["choix_menu"], bool=False)

        return next_view
