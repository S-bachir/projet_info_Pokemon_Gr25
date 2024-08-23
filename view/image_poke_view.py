from PyInquirer import prompt, Separator

from webservice.api_pokemon import ApiPokemon
from service.pokemon_service import PokemonService
from time_print import delay_print

from PIL import Image
import time


class ImagePokeView:
    def __init__(self):

        self.pokemons_objet = PokemonService.get_all_pokemons_from_db()
        self.pokemons_nom = [objet_poke.nom_poke for objet_poke in self.pokemons_objet]
        # Création du menu
        choix_pokemon = self.pokemons_nom
        choix_pokemon.append(Separator())
        choix_pokemon.append("Retour au menu principal")

        self.questions = [
            {
                'type': 'list',
                'name': 'choix_menu',
                'message': "Menu : Veuillez choisir un pokémon à afficher",
                'choices': choix_pokemon
            }
        ]

    def display_info(self):
        print("\t*******************")
        delay_print("\t*   Album Photo   *\n")
        print("\t*******************\n")
        time.sleep(3)

    def make_choice(self):

        reponse = prompt(self.questions)
        if reponse['choix_menu'] == 'Retour au menu principal':
            from view.menu_principal_view import MenuPrincipalView
            next_view = MenuPrincipalView()
        else:
            index = self.pokemons_nom.index(reponse["choix_menu"])
            objet_poke = self.pokemons_objet[index]
            img = ApiPokemon.get_image_poke(objet_poke.id_poke)
            image = Image.open(img.raw)
            image.show()
            next_view = ImagePokeView()

        return next_view
