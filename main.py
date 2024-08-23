from view.start_view import StartView
import pygame

import time
import sys


def delay_print(s):
    for c in s:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.001)


# C'est le script qui va être le point d'entrée de notre application.

if __name__ == '__main__':

    # on lance la musique

    pygame.mixer.pre_init(44100, -16, 2, 4096)
    pygame.mixer.init()
    pygame.mixer.music.load("music/pokemon_sound.ogg")
    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(0.3)

    # on démarre sur l'écran accueil
    current_vue = StartView()

    # tant qu'on a un écran à afficher, on continue
    while current_vue:
        # on affiche une bordure pour séparer les vue

        with open('assets/border', 'r', encoding="utf-8") as asset:
            print(asset.read())
        # les infos à afficher
        current_vue.display_info()
        # le choix que doit saisir l'utilisateur
        current_vue = current_vue.make_choice()

    with open('assets/close', 'r', encoding="utf-8") as asset:
        delay_print(asset.read())

    # stop de la musique
    pygame.mixer.music.stop()
    pygame.mixer.quit()
