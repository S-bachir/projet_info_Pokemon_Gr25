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


class CombatEquipeView(AbstractView):

    def __init__(self, dresseur_adverse, poke_dresseur, poke_dresseur_adverse):
        """
        :param dresseur_adverse: dresseur à affronter qui est un objet de type dresseur
        :type dresseur_adverse: Dresseur
        :param poke_dresseur: équipe de pokémon du dresseur joueur
        :type poke_dresseur: list
        :param poke_dresseur_adverse: équipe de pokémon du dresseur adverse
        :type poke_dresseur_adverse: list
        """
        self.dresseur_adverse = dresseur_adverse
        self.liste_poke_dresseur = poke_dresseur
        self.liste_poke_dresseur_adverse = poke_dresseur_adverse

        # les informations du dresseur joueur

        ids_poke = DresseurPokeService.get_id_poke_from_db(
            AbstractView.session.dresseur_actif.id_dresseur)

        # liste des pokemons associés à au dresseur
        pokemons_objet = [
            PokemonService.get_pokemon_from_db_by_id(id_poke[0]) for id_poke in ids_poke
        ]
        AbstractView.session.liste_poke_dresseur = pokemons_objet

        # Choisir et établir les informations du dresseur adverse

        dresseurs_affiches = DresseurService.get_all_dresseurs_from_db()

        # la liste avec uniquement les noms
        self.dresseurs_nom = [dresseur.nom_dresseur for dresseur in dresseurs_affiches]
        id_dresseurs_adverse = DresseurRencontreService.get_id_dresseur_adverse(
            AbstractView.session.dresseur_actif.id_dresseur
        )

        for id_dresseur in id_dresseurs_adverse:
            self.objet_dresseur_adverse = DresseurService.get_dresseur_by_id(id_dresseur)
            self.dresseurs_nom.remove(self.objet_dresseur_adverse.nom_dresseur)

        self.dresseurs_nom.remove(AbstractView.session.dresseur_actif.nom_dresseur)

        if len(self.dresseurs_nom) == 0:
            pass
        else:
            if self.dresseur_adverse is None:
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

                # liste des pokemons associés à un dresseur adverse
                pokemons_objet = [
                    PokemonService.get_pokemon_from_db_by_id(id_poke[0]) for id_poke in ids_poke
                ]
                AbstractView.session.liste_poke_dresseur_adverse = pokemons_objet
            else:
                pass

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
        if self.dresseur_adverse is None and len(self.dresseurs_nom) == 0:
            delay_print("Vous avez déjà défié tous les dresseurs!\n")
            next_view = MenuPrincipalView()

        else:

            if self.dresseur_adverse is None:
                delay_print("Vous venez de défier le dresseur {}\n".format(
                    self.choix_dresseur.upper()))
                self.dresseur_adverse = AbstractView.session.dresseur_adverse
                self.liste_poke_dresseur = AbstractView.session.liste_poke_dresseur
                self.liste_poke_dresseur_adverse = AbstractView.session.liste_poke_dresseur_adverse

            else:
                delay_print("Le combat continue avec {}\n".format(self.dresseur_adverse.nom_dresseur.upper()))
                time.sleep(2)

            poke_adverse = random.choice(self.liste_poke_dresseur_adverse)
            AbstractView.session.pokemon_adverse = poke_adverse

            objet_poke_adverse = AbstractView.session.pokemon_adverse
            id_poke_adverse = objet_poke_adverse.id_poke
            objet_dresseur = AbstractView.session.dresseur_actif

            delay_print("{} envoie le pokemon {}\n".format(
                self.dresseur_adverse.nom_dresseur.upper(), objet_poke_adverse.nom_poke))
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

                for poke in self.liste_poke_dresseur:
                    if poke.nom_poke == AbstractView.session.pokemon_actif.nom_poke:
                        AbstractView.session.pokemon_actif = poke

                objet_poke_actif = AbstractView.session.pokemon_actif
                id_poke_actif = objet_poke_actif.id_poke
                first_attack_poke = random.choice([id_poke_adverse, id_poke_actif])

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
                        print("\n\n{}".format(AbstractView.session.dresseur_actif.nom_dresseur).upper()
                              + '\033[31m' + "================"
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
                              + '\033[0m' + "{}".format(AbstractView.session.dresseur_adverse.nom_dresseur).upper()
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

                            self.liste_poke_dresseur_adverse.remove(objet_poke_adverse)
                            n = len(self.liste_poke_dresseur_adverse)
                            time.sleep(3)

                            if n > 0:
                                delay_print("\n\nCe n'est pas finie! {} a encore {} pokémons dans son équipe".format(
                                    self.dresseur_adverse.nom_dresseur.upper(), n))

                                next_view = CombatEquipeView(
                                    self.dresseur_adverse,
                                    self.liste_poke_dresseur,
                                    self.liste_poke_dresseur_adverse)
                            else:
                                delay_print("\n\nFélicitation!")
                                delay_print("\n\nVous venez de vaincre tous les pokémons de l'équipe de {}!".format(
                                    self.objet_dresseur_adverse.nom_dresseur.upper()))
                                AbstractView.session.dresseur_actif.argent += 1500
                                delay_print("\n\nVous recevez 1500 euros comme récompense!")
                                DresseurService.update_dresseur_in_db(AbstractView.session.dresseur_actif)
                                next_view = MenuPrincipalView()

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
                    print("\n\n{}".format(AbstractView.session.dresseur_actif.nom_dresseur).upper()
                          + '\033[31m' + "================"
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
                          + '\033[0m' + "{}".format(AbstractView.session.dresseur_adverse.nom_dresseur).upper()
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

                        self.liste_poke_dresseur.remove(objet_poke_actif)
                        AbstractView.session.liste_poke_dresseur = self.liste_poke_dresseur
                        n = len(self.liste_poke_dresseur)
                        time.sleep(3)

                        if n > 0:
                            delay_print(
                                "\n\nCe n'est pas finie! Il reste encore {} pokémons dans votre équipe !".format(n))

                            from view.choix_poke_combat_equipe import ChoixPokeCombat
                            next_view = ChoixPokeCombat()
                        else:
                            delay_print("\n\nVous avez perdu contre le dresseur {} !".format(
                                self.objet_dresseur_adverse.nom_dresseur.upper()))
                            AbstractView.session.dresseur_adverse.argent += 1500
                            delay_print("\n\n{} vient de gagner 1500 euros comme récompense !".format(
                                self.objet_dresseur_adverse.nom_dresseur.upper()
                            ))
                            DresseurService.update_dresseur_in_db(AbstractView.session.dresseur_adverse)
                            next_view = MenuPrincipalView()
                        break

        return next_view

    def display_info(self):
        if self.dresseur_adverse is None:
            print("\t**************",
                  "\n\t*   Combat   *",
                  "\n\t**************\n")
        pass
