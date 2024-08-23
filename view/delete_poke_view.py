
from PyInquirer import prompt, Separator

from service.pokemon_service import PokemonService
from service.dresseur_poke_service import DresseurPokeService
from view.abstract_vue import AbstractView
from time_print import delay_print


class DeletePokeView(AbstractView):

    def __init__(self):
        # la liste des pokemons que l'on affiche
        id_dresseur = AbstractView.session.dresseur_actif.id_dresseur
        ids_poke = DresseurPokeService.get_id_poke_from_db(id_dresseur)

        # liste des pokemons associés à un dresseur
        self.pokemons_objet = [
            PokemonService.get_pokemon_from_db_by_id(id_poke[0]) for id_poke in ids_poke
        ]
        self.pokemons_nom = [objet_poke.nom_poke for objet_poke in self.pokemons_objet]
        # Création du menu
        choix_pokemon = self.pokemons_nom
        AbstractView.session.liste_pokemon_dresseur = choix_pokemon
        choix_pokemon.append(Separator())
        choix_pokemon.append("Retour au menu principal")

        self.questions = [
            {
                'type': 'list',
                'name': 'choix_menu',
                'message': 'Menu : Veillez choisir un pokemon à supprimer:',
                'choices': choix_pokemon
            }
        ]

    def display_info(self):
        print("\t********************************",
              "\n\t*   Votre équipe de pokémons   *",
              "\n\t********************************\n")

    def make_choice(self):
        reponse = prompt(self.questions)
        if reponse["choix_menu"] == "Retour au menu principal":
            from view.menu_principal_view import MenuPrincipalView
            next_view = MenuPrincipalView()
        else:
            # Besoin de récupérer le pokemon avec son nom. On va aller vite
            # et se baser sur les index.
            index = self.pokemons_nom.index(reponse["choix_menu"])
            DresseurPokeService.delete_dresseur_poke(
                AbstractView.session.dresseur_actif,
                self.pokemons_objet[index])
            delay_print("Le pokemon vient d'être supprimer dans votre équipe")
            from view.menu_principal_view import MenuPrincipalView
            next_view = MenuPrincipalView()

        return next_view
