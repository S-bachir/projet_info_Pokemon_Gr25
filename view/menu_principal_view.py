from PyInquirer import prompt, Separator

from view.abstract_vue import AbstractView
from service.pokemon_service import PokemonService
from service.ball_service import BallService

from time_print import delay_print


class MenuPrincipalView(AbstractView):

    def __init__(self):
        self.questions = [
            {
                'type': 'list',
                'name': 'choix_menu',
                'message': 'Menu principal',
                'choices': [
                    "Choisir/Changer son pokémon principal",
                    "Affronter/Attraper un pokémon sauvage",
                    "Acheter des balls",
                    "Consulter son pokédex",
                    "Affronter des dresseurs de pokémons : Combat rapide solo",
                    "Affronter des dresseurs de pokémons : Combat normal",
                    "Supprimer des pokemons de son équipe",
                    "Afficher l'image d'un pokémon",
                    Separator(),
                    "Se déconnecter"
                ]
            }
        ]

    def make_choice(self):
        reponse = prompt(self.questions)
        if reponse['choix_menu'] == "Choisir/Changer son pokémon principal":
            from view.pokemons_liste_view import PokemonsListeView
            next_view = PokemonsListeView()

        elif reponse['choix_menu'] == "Affronter/Attraper un pokémon sauvage":
            try:
                assert AbstractView.session.pokemon_actif is not None
            except AssertionError:
                delay_print("\nVeuillez choisir un pokémon principal avant de partir au combat !")
                return MenuPrincipalView()

            AbstractView.session.adversaire = "pokemon sauvage"  # modif dans session adversaire
            from view.combat_poke_view import CombatPokeView
            next_view = CombatPokeView()

        elif reponse["choix_menu"] == "Acheter des balls":
            from view.achat_ball_view import AchatBallView
            next_view = AchatBallView()

        elif reponse["choix_menu"] == "Consulter son pokédex":
            from view.pokedex_view import PokedexView
            next_view = PokedexView()

        elif reponse["choix_menu"] == "Affronter des dresseurs de pokémons : Combat rapide solo":
            try:
                assert AbstractView.session.pokemon_actif is not None
            except AssertionError:
                delay_print("\nVeuillez choisir un pokémon principal avant de partir au combat !")
                return MenuPrincipalView()
            AbstractView.session.adversaire = "dresseur"  # modif dans session adversaire
            from view.combat_poke_view import CombatPokeView
            next_view = CombatPokeView()
        elif reponse["choix_menu"] == "Affronter des dresseurs de pokémons : Combat normal":
            try:
                assert AbstractView.session.pokemon_actif is not None
            except AssertionError:
                delay_print("\nVeuillez choisir un pokémon principal avant de partir au combat !")
                return MenuPrincipalView()
            AbstractView.session.adversaire = "dresseur"  # modif dans session adversaire
            from view.combat_equipe_view import CombatEquipeView
            next_view = CombatEquipeView(None, None, None)

        elif reponse["choix_menu"] == "Supprimer des pokemons de son équipe":
            from view.delete_poke_view import DeletePokeView
            next_view = DeletePokeView()

        elif reponse["choix_menu"] == "Afficher l'image d'un pokémon":
            from view.image_poke_view import ImagePokeView
            next_view = ImagePokeView()

        else:
            from view.welcome_view import WelcomeView
            next_view = WelcomeView()

        return next_view

    def display_info(self):
        print("\t**********************",
              "\n\t*   Menu Principal   *",
              "\n\t**********************\n")
        if AbstractView.session.pokemon_actif is None:
            delay_print('Bienvenue {}, content de vous savoir parmi nous!\n\n'.format(
                AbstractView.session.user_name))

        else:
            pass

        nom_poke = AbstractView.session.dresseur_actif.pokemon_actif
        AbstractView.session.pokemon_actif = PokemonService.get_pokemon_by_name(nom_poke)
        delay_print("Nom du dresseur actif : {}\n".format(AbstractView.session.dresseur_actif.nom_dresseur))
        delay_print("Son identifiant : {}\n".format(
            AbstractView.session.dresseur_actif.id_dresseur))
        delay_print("Son argent: {}\n".format(
            AbstractView.session.dresseur_actif.argent))
        balls_nom = BallService.get_all_balls_from_db(
            AbstractView.session.dresseur_actif.id_dresseur
        )
        balls = ""
        for ball in balls_nom:
            balls = balls + " | " + ball
        delay_print("Balls en sa possession : {}\n".format(balls))
        print(Separator())
        delay_print("son pokemon actif : {}\n".format(
            AbstractView.session.dresseur_actif.pokemon_actif))
        if AbstractView.session.pokemon_actif is not None:
            delay_print('point de vie : {}\n'.format(AbstractView.session.pokemon_actif.pv))
            delay_print('Niveau d\'expérience : {}\n'.format(AbstractView.session.pokemon_actif.niveau_exp))
            delay_print('Type de pokémon : {}\n\n'.format(
                PokemonService.get_type_translate(AbstractView.session.pokemon_actif.type_poke)))
        pass
