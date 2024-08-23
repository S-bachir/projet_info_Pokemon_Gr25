from PyInquirer import Separator, prompt

from view.abstract_vue import AbstractView
from webservice.api_pokemon import ApiPokemon
from time_print import delay_print

from PIL import Image
import psutil
import time


class PokemonView(AbstractView):
    def __init__(self):
        self.questions = [
            {
                'type': 'list',
                'name': 'menu',
                'message': 'Que voulez vous faire ? :',
                'choices': [
                    'Retour au menu principal'
                ]
            }
        ]

    def display_info(self):
        delay_print("Nom du pokemon : {}".format(
            AbstractView.session.pokemon_actif.nom_poke))
        delay_print("\nSon identifiant : {}".format(
            AbstractView.session.pokemon_actif.id_poke))
        delay_print("\ntype pokemon : {}".format(
            ApiPokemon.get_french_translate_type_name(AbstractView.session.pokemon_actif.type_poke)))
        delay_print("\nPoint de vie: {}".format(
            AbstractView.session.pokemon_actif.pv))
        delay_print("\nniveau d'expérience : {}".format(
            AbstractView.session.pokemon_actif.niveau_exp))
        delay_print("\nvitesse : {}".format(
            AbstractView.session.pokemon_actif.vitesse))
        delay_print("\nDéfense : {}\n".format(
            AbstractView.session.pokemon_actif.defense))

        img = ApiPokemon.get_image_poke(AbstractView.session.pokemon_actif.id_poke)
        image = Image.open(img.raw)
        image.show()
        #with Image.open(image.raw) as img:
         #   img.show()
          #  time.sleep(3)
           # for proc in psutil.process_iter():
            #    if proc.name() == "display":
             #       proc.kill()
        
    def make_choice(self):
        reponse = prompt(self.questions)
        if reponse["menu"] == 'Retour au menu principal':
            from view.menu_principal_view import MenuPrincipalView
            return MenuPrincipalView()
