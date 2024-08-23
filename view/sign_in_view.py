from PyInquirer import Separator, prompt, Validator, ValidationError

from view.abstract_vue import AbstractView
from service.utilisateur_service import UtilisateurService
from service.dresseur_service import DresseurService
from service.dresseur_poke_service import DresseurPokeService
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


class SignInView(AbstractView):
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
        from view.welcome_view import WelcomeView

        reponse1 = prompt(self.questions_pseudo)
        try:
            pseudo = UtilisateurService.get_user_by_name(reponse1['pseudonyme'])[0]
            if reponse1['pseudonyme'] == pseudo:
                AbstractView.session.user_name = reponse1['pseudonyme']

            else:
                pass

            reponse2 = prompt(self.questions_mdp)
            mdp_sign = reponse2['mot de passe'].encode()
            mdp_sign_hash = sha1(mdp_sign).hexdigest()
            mdp_hash = UtilisateurService.get_user_by_name(reponse1['pseudonyme'])[1]
            if mdp_sign_hash == mdp_hash:
                AbstractView.session.user_mdp = reponse2['mot de passe']

                AbstractView.session.dresseur_actif = DresseurService.get_dresseur_by_user(
                    AbstractView.session.user_name
                )

                from view.menu_principal_view import MenuPrincipalView
                next_view = MenuPrincipalView()
            else:
                delay_print("\nMot de passe incorrect.")
                next_view = WelcomeView()
        except TypeError:
            delay_print("\nL'utilisateur {} n'existe pas dans la base de donnée.".format(
                reponse1['pseudonyme']
            ))
            next_view = WelcomeView()

        return next_view
