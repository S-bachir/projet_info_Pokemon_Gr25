from service.pokemon_service import PokemonService

from time_print import delay_print


class CombatService:

    def __init__(self):
        pass

    @staticmethod
    def get_attack(pokemon_qui_attaque, nom_attaque, pokemon_qui_defend):
        cm = 1
        """
        Pour le calcul on s'est servi du site : https://www.pokepedia.fr/Calcul_des_d%C3%A9g%C3%A2ts
        Méthode qui permet de lancer une attaque
        :type pokemon: Pokemon
        :type id_poke_adverse: int
        :rtype:int
        """

        if PokemonService.get_double_damage_to(pokemon_qui_attaque.type_poke, pokemon_qui_defend.type_poke):
            cm *= 2
            delay_print("L'attaque du pokémon {} est super efficace car le type {} a l'ascendant sur {}\n".format(
                pokemon_qui_attaque.nom_poke,
                PokemonService.get_type_translate(pokemon_qui_attaque.type_poke),
                PokemonService.get_type_translate(pokemon_qui_defend.type_poke)))

        elif PokemonService.get_half_damage_to(pokemon_qui_attaque.type_poke, pokemon_qui_defend.type_poke):
            cm *= 1 / 2
            delay_print("L'attaque du pokémon {} n'est pas très efficace car le type {} a l'ascendant sur {}\n".format(
                pokemon_qui_attaque.nom_poke,
                PokemonService.get_type_translate(pokemon_qui_defend.type_poke),
                PokemonService.get_type_translate(pokemon_qui_attaque.type_poke)))

        puissance = PokemonService.get_puissance_attack(nom_attaque)
        attaque = PokemonService.get_power_attack(nom_attaque)
        degats_attaque = round(((puissance * attaque * (0.4 * pokemon_qui_attaque.niveau_exp + 2)) / (
                pokemon_qui_defend.defense * 50) + 2) * cm)
        delay_print("\n-> Nom d'attaque : {}".format(PokemonService.get_atatque_translate(nom_attaque)))
        delay_print("\n-> Capacité d'attaque de {} points".format(attaque))
        return degats_attaque

    @staticmethod
    def get_defense(pokemon, degat_attaque):
        """
        Méthode qui permet de se défendre
        :type pokemon: Pokemon
        :type degat_attaque: int
        :rtype:int
        """
        print(pokemon.description_defense)
        delay_print("\nCapacité de défense total de {} points".format(
            degat_attaque - pokemon.utiliser_defense(degat_attaque)))
        delay_print("\nLes dégats finaux sont de l'ordre de {} points".format(
            pokemon.utiliser_defense(degat_attaque)
        ))
        input("\n_>")
        return pokemon.utiliser_defense(degat_attaque)
