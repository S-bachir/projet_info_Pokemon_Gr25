from PyInquirer import prompt, Separator

from view.abstract_vue import AbstractView
from time_print import delay_print


class WelcomeView(AbstractView):

    def __init__(self):
        self.questions = [
            {
                'type': 'list',
                'name': 'choix_menu',
                'message': 'Menu',
                'choices': [
                    "Créer un compte",
                    "se connecter",
                    Separator(),
                    "Quitter l'application"
                ]
            }
        ]

    def make_choice(self):
        reponse = prompt(self.questions)
        if reponse['choix_menu'] == 'Créer un compte':
            from view.create_account_view import CreateAccountView
            next_view = CreateAccountView()
        elif reponse["choix_menu"] == 'se connecter':
            from view.sign_in_view import SignInView
            next_view = SignInView()
        else:
            next_view = None
        return next_view

    def display_info(self):
        if AbstractView.session.dresseur_actif is None and AbstractView.session.pokemon_actif is None:
            delay_print('Vous allez entrer dans le monde du jeu pokemon !')

        else:
            pass
