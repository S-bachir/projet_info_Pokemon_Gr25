from PyInquirer import prompt, Separator

from view.abstract_vue import AbstractView
from dao.pokemon_dao import PokemonDao
from webservice.api_pokemon import ApiPokemon
from service.dresseur_poke_service import DresseurPokeService
from service.pokemon_service import PokemonService
from PIL import Image

from time_print import delay_print


class StatPokeView(AbstractView):

    def __init__(self, name_pokemon, bool):
        self.name_pokemon = name_pokemon
        self.bool = bool

        if self.bool is True:
            self.questions = [
                {
                    'type': 'list',
                    'name': 'choix_menu',
                    'message': 'retour:',
                    'choices': [
                        'Ajouter le pokémon dans son équipe',
                        'Retour dans le pokédex',
                        Separator(),
                        'Retour au menu principal'
                    ]

                }
            ]

        else:
            self.questions = [
                {
                    'type': 'list',
                    'name': 'choix_menu',
                    'message': 'retour:',
                    'choices': [
                        'Retour dans le pokédex',
                        Separator(),
                        'Retour au menu principal'
                    ]

                }
            ]

    def display_info(self):
        print("""        
                         Le nom du pokemon :                  {}
                         Son type/element:                    {}  
                         Le niveau d'expérience du pokemon :  {}
                         Ses points de vie :                  {}
                         Sa vitesse :                         {}
                         Sa defense :                         {}
                         ses différents moves d'attaque :     {}
                                                              {}
                                                              {}
                                                              {}    

                                """.format(
            PokemonDao.find_by_name(self.name_pokemon).nom_poke,
            ApiPokemon.get_french_translate_type_name(PokemonDao.find_by_name(self.name_pokemon).type_poke),
            PokemonDao.find_by_name(self.name_pokemon).niveau_exp,
            PokemonDao.find_by_name(self.name_pokemon).pv,
            PokemonDao.find_by_name(self.name_pokemon).vitesse,
            PokemonDao.find_by_name(self.name_pokemon).defense,
            ApiPokemon.get_french_translate_attaque_name(PokemonDao.find_by_name(self.name_pokemon).nom_attaque_1),
            ApiPokemon.get_french_translate_attaque_name(PokemonDao.find_by_name(self.name_pokemon).nom_attaque_2),
            ApiPokemon.get_french_translate_attaque_name(PokemonDao.find_by_name(self.name_pokemon).nom_attaque_3),
            ApiPokemon.get_french_translate_attaque_name(PokemonDao.find_by_name(self.name_pokemon).nom_attaque_4),
        ))
        objet_poke = PokemonService.get_pokemon_by_name(name_poke=self.name_pokemon)
        img = ApiPokemon.get_image_poke(objet_poke.id_poke)
        image = Image.open(img.raw)
        image.show()

    def make_choice(self):

        reponse = prompt(self.questions)
        if reponse['choix_menu'] == 'Ajouter le pokémon dans son équipe':
            # la liste des pokemons que l'on affiche
            id_dresseur = AbstractView.session.dresseur_actif.id_dresseur
            ids_poke = DresseurPokeService.get_id_poke_from_db(id_dresseur)

            # liste des pokemons associés à un dresseur
            pokemons_objet = [
                PokemonService.get_pokemon_from_db_by_id(id_poke[0]) for id_poke in ids_poke
            ]
            pokemons_nom = [objet_poke.nom_poke for objet_poke in pokemons_objet]

            if self.name_pokemon in pokemons_nom:
                delay_print("Le pokémon existe déjà dans votre équipe !")

            else:
                object_poke = PokemonDao.find_by_name(self.name_pokemon)
                DresseurPokeService.add_dresseur_poke_in_bd(
                    AbstractView.session.dresseur_actif,
                    object_poke
                )
                delay_print("\nLe pokemon {} vient d'être ajouter à votre liste de pokémons".format(
                    self.name_pokemon
                ))

            from view.pokedex_view import PokedexView
            next_view = PokedexView()

        elif reponse['choix_menu'] == 'Retour dans le pokédex':
            from view.pokedex_view import PokedexView
            next_view = PokedexView()

        else:
            from view.menu_principal_view import MenuPrincipalView
            next_view = MenuPrincipalView()

        return next_view
