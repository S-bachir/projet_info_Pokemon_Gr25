from PyInquirer import Separator, prompt, Validator, ValidationError

from view.abstract_vue import AbstractView
from service.utilisateur_service import UtilisateurService
from hashlib import sha1

from time_print import delay_print


class PasswordValidator(Validator):
    @staticmethod
    def validate(document):
        ok = len(document.text) > 5
        if not ok:
            raise ValidationError(
                message='Votre mot de passe doit faire au moins 6 caractères',
                cursor_position=len(document.text))  # Move cursor to end


class CreateAccountView(AbstractView):
    def __init__(self):
        self.questions_pseudo = [
            {
                'type': 'input',
                'name': 'pseudonyme',
                'message': 'Quel est votre pseudonyme ?',

            }
        ]
        self.questions_mdp = [
            {
                'type': 'password',
                'name': 'mot de passe',
                'message': 'Quel est votre mot de passe ?',
                'validate': PasswordValidator
            }
        ]

    def display_info(self):
        pass

    def make_choice(self):
        from view.menu_principal_view import MenuPrincipalView
        from view.welcome_view import WelcomeView

        reponse1 = prompt(self.questions_pseudo)
        boolean = reponse1['pseudonyme'] in UtilisateurService.get_all_user()
        if boolean is False:
            AbstractView.session.user_name = reponse1['pseudonyme']
            reponse2 = prompt(self.questions_mdp)
            mdp = reponse2["mot de passe"].encode()
            mdp_hash = sha1(mdp).hexdigest()
            UtilisateurService.add_user_in_db(
                reponse1["pseudonyme"],
                mdp_hash
            )

            delay_print("\nCréation de l'utilisateur {} valide!".format(
                reponse1["pseudonyme"]
            ))
            AbstractView.session.user_name = reponse1['pseudonyme']
            from view.dresseurs_liste_view import DresseursListeView
            next_view = DresseursListeView()

        else:
            delay_print("\nl'utilisateur {} existe déjà!".format(
                reponse1['pseudonyme']
            ))
            next_view = WelcomeView()

        return next_view
