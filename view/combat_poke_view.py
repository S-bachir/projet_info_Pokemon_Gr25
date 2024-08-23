from typing import Dict, Any

from PyInquirer import prompt, Separator

from view.abstract_vue import AbstractView
import random

from metier.pokedex import Pokedex
from service.pokemon_service import PokemonService
from service.pokedex_service import PokedexService
from service.dresseur_service import DresseurService
from service.dresseur_poke_service import DresseurPokeService
from service.dresseur_renc_service import DresseurRencontreService
from service.combat_service import CombatService

from time_print import delay_print

from webservice.api_pokemon import ApiPokemon
from PIL import Image
import psutil
import time


class CombatPokeView(AbstractView):

    def __init__(self):

        if AbstractView.session.adversaire == "pokemon sauvage":
            self.id_poke_adverse = random.randrange(22, 121, 2)

        elif AbstractView.session.adversaire == "dresseur":

            dresseurs_affiches = DresseurService.get_all_dresseurs_from_db()

            # la liste avec uniquement les noms
            self.dresseurs_nom = [dresseur.nom_dresseur for dresseur in dresseurs_affiches]
            id_dresseurs_adverse = DresseurRencontreService.get_id_dresseur_adverse(
                AbstractView.session.dresseur_actif.id_dresseur
            )

            for id_dresseur in id_dresseurs_adverse:
                objet_dresseur_adverse = DresseurService.get_dresseur_by_id(id_dresseur)
                self.dresseurs_nom.remove(objet_dresseur_adverse.nom_dresseur)

            self.dresseurs_nom.remove(AbstractView.session.dresseur_actif.nom_dresseur)

            if len(self.dresseurs_nom) == 0:
                pass
            else:
                self.choix_dresseur = random.choice(self.dresseurs_nom)
                AbstractView.session.dresseur_adverse = DresseurService.get_id_dresseur_by_name(
                    self.choix_dresseur)

                DresseurRencontreService.add_dresseurs_rencontre(
                    AbstractView.session.dresseur_actif,
                    AbstractView.session.dresseur_adverse
                )

                id_dresseur = \
                    DresseurService.get_id_dresseur_by_name(
                        self.choix_dresseur).id_dresseur
                ids_poke = DresseurPokeService.get_id_poke_from_db(id_dresseur)

                # liste des pokemons associés à un dresseur
                pokemons_objet = [
                    PokemonService.get_pokemon_from_db_by_id(id_poke[0]) for id_poke in ids_poke
                ]
                self.id_poke_adverse = random.choice(pokemons_objet).id_poke

        pokemon = AbstractView.session.pokemon_actif
        choix_attaque_poke_actif = [PokemonService.get_atatque_translate(pokemon.nom_attaque_1),
                                    PokemonService.get_atatque_translate(pokemon.nom_attaque_2),
                                    PokemonService.get_atatque_translate(pokemon.nom_attaque_3),
                                    PokemonService.get_atatque_translate(pokemon.nom_attaque_4),
                                    Separator(), "Quitter le combat"]

        self.choix_attack_dict = {PokemonService.get_atatque_translate(pokemon.nom_attaque_1): pokemon.nom_attaque_1,
                                  PokemonService.get_atatque_translate(pokemon.nom_attaque_2): pokemon.nom_attaque_2,
                                  PokemonService.get_atatque_translate(pokemon.nom_attaque_3): pokemon.nom_attaque_3,
                                  PokemonService.get_atatque_translate(pokemon.nom_attaque_4): pokemon.nom_attaque_4}

        self.questions = [
            {
                'type': 'list',
                'name': 'choix_menu',
                'message': 'Menu : Choisissez une attaque',
                'choices': choix_attaque_poke_actif
            }
        ]

    def make_choice(self):

        from view.menu_principal_view import MenuPrincipalView
        next_view = MenuPrincipalView()
        if AbstractView.session.adversaire == "dresseur" and len(self.dresseurs_nom) == 0:
            delay_print("Vous avez déjà défié tous les dresseurs!\n")
            next_view = MenuPrincipalView()

        else:
            objet_poke_adverse = PokemonService.get_pokemon_from_db_by_id(self.id_poke_adverse)
            objet_dresseur = AbstractView.session.dresseur_actif
            if AbstractView.session.adversaire == "dresseur":
                delay_print("Vous venez de défier le dresseur {}\n".format(
                    self.choix_dresseur.upper()))
                delay_print("{} envoie le pokemon {}\n".format(
                    self.choix_dresseur.upper(), objet_poke_adverse.nom_poke))

            else:
                delay_print("\nVous allez affronter le pokemon : {}\n".format(objet_poke_adverse.nom_poke))

            delay_print("Niveau d'expérience : {}\n".format(objet_poke_adverse.niveau_exp))
            delay_print("Type de pokémon : {}\n".format(
                PokemonService.get_type_translate(objet_poke_adverse.type_poke)))

            img = ApiPokemon.get_image_poke(objet_poke_adverse.id_poke)
            image = Image.open(img.raw)
            image.show()
            #with Image.open(image.raw) as img:
             #   img.show()
              #  time.sleep(3)
               # for proc in psutil.process_iter():
                #    if proc.name() == "display":
                 #       proc.kill()

            if (objet_dresseur.id_dresseur, "R") not in PokedexService.get_all_pokedex():
                PokedexService.add_pokemon_to_pokedex(
                    AbstractView.session.dresseur_actif, Pokedex(), "R")

            pokedex_r = PokedexService.get_all_pokemons_r(objet_dresseur)
            PokedexService.update_pokemon_in_pokedex(
                pokedex_r, objet_poke_adverse)

            while True:
                objet_poke_actif = AbstractView.session.pokemon_actif
                id_poke_actif = objet_poke_actif.id_poke
                first_attack_poke = random.choice([self.id_poke_adverse, id_poke_actif])

                if first_attack_poke == id_poke_actif:
                    delay_print("\nLe pokemon {} attaque\n\n".format(objet_poke_actif.nom_poke))
                    reponse = prompt(self.questions)

                    if reponse["choix_menu"] == "Quitter le combat":
                        next_view = MenuPrincipalView()
                        break
                    else:

                        degats_finaux = CombatService.get_attack(objet_poke_actif,
                                                                 self.choix_attack_dict[reponse["choix_menu"]],
                                                                 objet_poke_adverse)

                        delay_print("\n\nLe pokemon {} défend".format(objet_poke_adverse.nom_poke))
                        delay_print("\n-> Capacité de défense de {} points".format(objet_poke_adverse.defense))
                        delay_print("\n\n****** {} points de dégats infligés ******".format(degats_finaux))

                        objet_poke_adverse.pv = objet_poke_adverse.pv - degats_finaux

                        if objet_poke_adverse.pv < 0:
                            objet_poke_adverse.pv = 0
                        print('\033[31m' + "\n\n================"
                              + '\033[0m' + "{}".format(objet_poke_actif.nom_poke)
                              + '\033[31m' + "====="
                              + '\033[0m' + "{}".format(objet_poke_actif.pv)
                              + '\033[31m' + "========="
                              + '\033[0m'
                              + '\033[33m' + '\033[1m' + "VS"
                              + '\033[0m'
                              + '\033[31m' + "========="
                              + '\033[0m' + "{}".format(objet_poke_adverse.pv)
                              + '\033[31m' + "====="
                              + '\033[0m' + "{}".format(objet_poke_adverse.nom_poke)
                              + '\033[31m' + "================"
                              )
                        print('\033[0m')
                        if objet_poke_adverse.pv > 0:
                            continue
                        else:
                            delay_print("\nLe pokemon {} est K.O!".format(objet_poke_adverse.nom_poke))
                            delay_print("\nLe pokemon {} a gagné!".format(objet_poke_actif.nom_poke))
                            objet_poke_actif.niveau_exp = round(
                                objet_poke_actif.niveau_exp + (0.1 * objet_poke_adverse.niveau_exp))
                            PokemonService.update_pokemon_in_db(objet_poke_actif)

                            if AbstractView.session.adversaire == "dresseur":
                                AbstractView.session.dresseur_actif.argent +=\
                                    AbstractView.session.dresseur_adverse.argent
                                delay_print("\n\nVous venez de gagner {} euros.".format(
                                    AbstractView.session.dresseur_adverse.argent
                                ))

                                next_view = MenuPrincipalView()

                            else:
                                from view.capture_poke_view import CapturePokeView
                                next_view = CapturePokeView(objet_poke_adverse)

                            DresseurService.update_dresseur_in_db(
                                AbstractView.session.dresseur_actif
                            )

                            break

                else:
                    delay_print("\nLe pokemon {} attaque\n".format(objet_poke_adverse.nom_poke))
                    choix_attaque_poke_adverse = random.choice([
                        objet_poke_adverse.nom_attaque_1,
                        objet_poke_adverse.nom_attaque_2,
                        objet_poke_adverse.nom_attaque_3,
                        objet_poke_adverse.nom_attaque_4
                    ])
                    degats_finaux = CombatService.get_attack(objet_poke_adverse, choix_attaque_poke_adverse,
                                                             objet_poke_actif)
                    delay_print("\n\nLe pokemon {} défend".format(objet_poke_actif.nom_poke))
                    delay_print("\n-> Capacité de défense de {} points".format(objet_poke_actif.defense))
                    delay_print("\n\n****** {} points de dégats infligés ******".format(degats_finaux))

                    objet_poke_actif.pv = objet_poke_actif.pv - degats_finaux

                    if objet_poke_actif.pv < 0:
                        objet_poke_actif.pv = 0
                    print('\033[31m' + "\n\n================"
                          + '\033[0m' + "{}".format(objet_poke_actif.nom_poke)
                          + '\033[31m' + "====="
                          + '\033[0m' + "{}".format(objet_poke_actif.pv)
                          + '\033[31m' + "========="
                          + '\033[0m'
                          + '\033[33m' + '\033[1m' + "VS"
                          + '\033[0m'
                          + '\033[31m' + "========="
                          + '\033[0m' + "{}".format(objet_poke_adverse.pv)
                          + '\033[31m' + "====="
                          + '\033[0m' + "{}".format(objet_poke_adverse.nom_poke)
                          + '\033[31m' + "================"
                          )
                    print('\033[0m')
                    if objet_poke_actif.pv > 0:
                        continue
                    else:
                        delay_print("\nLe pokemon {} est K.O!".format(objet_poke_actif.nom_poke))
                        delay_print("\nLe pokemon {} a gagné!".format(objet_poke_adverse.nom_poke))
                        objet_poke_adverse.niveau_exp = round(
                            objet_poke_adverse.niveau_exp + (0.1 * objet_poke_actif.niveau_exp))
                        PokemonService.update_pokemon_in_db(objet_poke_adverse)

                        if AbstractView.session.adversaire == "dresseur":
                            AbstractView.session.dresseur_adverse.argent +=\
                                AbstractView.session.dresseur_actif.argent
                            delay_print("\n\nLe Dresseur adverse {} vient de gagner {} euros.".format(
                                self.choix_dresseur.upper(), AbstractView.session.dresseur_actif.argent
                            ))

                        else:
                            pass

                        DresseurService.update_dresseur_in_db(
                            AbstractView.session.dresseur_actif
                        )

                        next_view = MenuPrincipalView()
                        break

        return next_view

    def display_info(self):
        print("\t**************",
              "\n\t*   Combat   *",
              "\n\t**************\n")
