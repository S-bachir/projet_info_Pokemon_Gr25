from PyInquirer import prompt, Separator

from view.abstract_vue import AbstractView

import time
import sys


def delay_print(s):
    for c in s:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.0007)


class StartView(AbstractView):

    def __init__(self):
        self.questions = [
            {
                'type': 'list',
                'name': 'choix',
                'message': 'Bonjour! Veuillez choisir \"Next\" pour commencer',
                'choices': [
                    'Next'

                ]
            }
        ]

    def display_info(self):
        with open('assets/open', 'r', encoding="utf-8") as asset:
            delay_print(asset.read())

    def make_choice(self):
        reponse = prompt(self.questions)
        if reponse['choix'] == 'Next':
            from view.welcome_view import WelcomeView
            return WelcomeView()
