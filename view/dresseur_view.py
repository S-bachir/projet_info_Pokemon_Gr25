from PyInquirer import Separator, prompt

from view.abstract_vue import AbstractView


class DresseurView(AbstractView):
    def __init__(self):
        self.questions = [
            {
                'type': 'list',
                'name': 'menu',
                'message': 'Que voulez vous faire ? :',
                'choices': [
                    'Aller au menu principal',
                    Separator(),
                    'Se déconnecter'
                ]
            }
        ]

    def display_info(self):
        print("Nom du dresseur : {}".format(AbstractView.session.dresseur_actif.nom_dresseur))
        print("Son identifiant : {}".format(
            AbstractView.session.dresseur_actif.id_dresseur))
        print("Son argent: {}".format(
            AbstractView.session.dresseur_actif.argent))
        print("Le pokemon actif : {}".format(
            AbstractView.session.dresseur_actif.pokemon_actif))

    def make_choice(self):
        reponse = prompt(self.questions)
        if reponse["menu"] == "Aller au menu principal":
            from view.menu_principal_view import MenuPrincipalView
            next_view = MenuPrincipalView()
        else:
            from view.welcome_view import WelcomeView
            next_view = WelcomeView()

        return next_view
