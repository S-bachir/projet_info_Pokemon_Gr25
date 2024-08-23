from PyInquirer import prompt, Separator

from view.abstract_vue import AbstractView
import random

from metier.pokedex import Pokedex
from service.pokemon_service import PokemonService
from service.pokedex_service import PokedexService
from service.dresseur_service import DresseurService
from service.dresseur_poke_service import DresseurPokeService
from service.dresseur_renc_service import DresseurRencontreService
from service.combat_service import CombatService

from time_print import delay_print

from webservice.api_pokemon import ApiPokemon
from PIL import Image
import psutil
import time


# c'est ici que ça commence

class ChoixPokeCombat(AbstractView):

    def __init__(self):
        self.dresseur_adverse = AbstractView.session.dresseur_adverse
        self.liste_poke_dresseur = AbstractView.session.liste_poke_dresseur
        self.liste_poke_dresseur_adverse = AbstractView.session.liste_poke_dresseur_adverse

        self.poke_names = [pokemon.nom_poke for pokemon in self.liste_poke_dresseur]
        self.questions = [
            {
                'type': 'list',
                'name': 'choix_menu',
                'message': 'Menu : Veuillez choisir un nouveau pokémon pour continuer le combat',
                'choices': self.poke_names + [Separator(), ] + ["Quitter le combat"]
            }
        ]

    def make_choice(self):

        reponse = prompt(self.questions)

        if reponse["choix_menu"] in self.poke_names:
            i = self.poke_names.index(reponse["choix_menu"])
            objet_poke = self.liste_poke_dresseur[i]
            AbstractView.session.pokemon_actif = objet_poke

            from view.combat_equipe_view import CombatEquipeView
            delay_print("\n C'est au tour de {} de rejoindre le combat".format(reponse["choix_menu"]))
            next_view = CombatEquipeView(
                self.dresseur_adverse,
                self.liste_poke_dresseur,
                self.liste_poke_dresseur_adverse
            )

            image = ApiPokemon.get_image_poke(objet_poke.id_poke)
            with Image.open(image.raw) as img:
                img.show()
                time.sleep(3)
                for proc in psutil.process_iter():
                    if proc.name() == "display":
                        proc.kill()

        else:
            from view.menu_principal_view import MenuPrincipalView
            next_view = MenuPrincipalView()

        return next_view

    def display_info(self):
        names = ""
        for nom in self.poke_names:
            names = names + "  " + nom
        delay_print("Vos pokémons encore en état de combattre : {}\n\n".format(names))
