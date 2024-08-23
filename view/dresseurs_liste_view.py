from PyInquirer import prompt, Separator

from service.dresseur_service import DresseurService
from view.abstract_vue import AbstractView


class DresseursListeView(AbstractView):

    def __init__(self):
        # la liste des dresseurs que l'on affiche
        self.dresseurs_affiches = \
            DresseurService.get_all_dresseurs_none_user()
        # la liste avec uniquement les noms
        self.dresseur_nom = [dresseur.nom_dresseur for dresseur in
                             self.dresseurs_affiches]

        # Création du menu
        choix_dresseur = self.dresseur_nom
        choix_dresseur.append(Separator())
        self.questions = [
            {
                'type': 'list',
                'name': 'dresseurs',
                'message': 'Veillez choisir un dresseur :',
                'choices': choix_dresseur
            }
        ]

    def display_info(self):
        pass

    def make_choice(self):
        reponse = prompt(self.questions)
        AbstractView.session.dresseur_actif = reponse["dresseurs"]

        # Besoin de récupérer le dresseur avec son nom.
        # On va se baser sur les index.
        index = self.dresseur_nom.index(reponse["dresseurs"])
        AbstractView.session.dresseur_actif = \
            self.dresseurs_affiches[index]
        AbstractView.session.dresseur_actif.pseudo_user = AbstractView.session.user_name
        DresseurService.update_dresseur_in_db(AbstractView.session.dresseur_actif)
        from view.dresseur_view import DresseurView
        next_view = DresseurView()

        return next_view
