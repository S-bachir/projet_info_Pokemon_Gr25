from webservice.api_pokemon import ApiPokemon
from dao.pokemon_dao import PokemonDao


class PokemonService:

    def __init__(self):
        pass

    @staticmethod
    def get_pokemon_from_db_by_id(id_pokemon):
        """
        Récupère un pokemon grâce à son nom
        :param id_pokemon:
        :type id_pokemon:
        :return:
        :rtype:
        """
        return PokemonDao.find_by_id(id_pokemon)

    @staticmethod
    def get_pokemon_by_name(name_poke):
        return PokemonDao.find_by_name(name_poke)

    @staticmethod
    def get_info_poke_by_id(id_pokemon):
        return ("""Le nom du pokemon :                  {}
                 Son type/element:                    {}  
                 Le niveau d'expérience du pokemon :  {}
                 Ses points de vie :                  {}
                 Sa vitesse :                         {}
                 Sa defense :                         {}
                 ses différents moves d'attaque :     {}
                                                      {}
                                                      {}
                                                      {}    
        
        """.format(
            PokemonDao.find_by_id(id_pokemon).nom_poke,
            PokemonDao.find_by_id(id_pokemon).type_poke,
            PokemonDao.find_by_id(id_pokemon).niveau_exp,
            PokemonDao.find_by_id(id_pokemon).pv,
            PokemonDao.find_by_id(id_pokemon).vitesse,
            PokemonDao.find_by_id(id_pokemon).defense,
            PokemonDao.find_by_id(id_pokemon).nom_attaque_1,
            PokemonDao.find_by_id(id_pokemon).nom_attaque_2,
            PokemonDao.find_by_id(id_pokemon).nom_attaque_3,
            PokemonDao.find_by_id(id_pokemon).nom_attaque_4,
        ))

    @staticmethod
    def get_all_pokemons_from_db():
        """
        Récupère un certain nombre de pokemon en base
        :return: une liste de pokemon
        :rtype: list of Pokemon
        """
        return PokemonDao.find_all()

    @staticmethod
    def add_pokemon_to_db(pokemon):
        """

        :param pokemon:
        :type pokemon:
        :return:
        :rtype:
        """

        return PokemonDao.create(pokemon)

    @staticmethod
    def update_pokemon_in_db(pokemon):
        """

        :param pokemon:
        :type pokemon:
        :return:
        :rtype:
        """
        return PokemonDao.update(pokemon)

    @staticmethod
    def delete_pokemon_from_db_with_name(pokemon_name):
        return PokemonDao.delete(pokemon_name)

    @staticmethod
    def get_puissance_attack(name_attack):
        return ApiPokemon.get_puissance_attaque(name_attack)

    @staticmethod
    def get_power_attack(name_attack):
        return ApiPokemon.get_power_attaque(name_attack)

    @staticmethod
    def get_atatque_translate(nom_attack):
        return ApiPokemon.get_french_translate_attaque_name(nom_attack)

    @staticmethod
    def get_type_translate(nom_type):
        return ApiPokemon.get_french_translate_type_name(nom_type)

    @staticmethod
    def get_double_damage_from(type_qui_defend, type_qui_attaque):
        """
        Est ce que le pokémoon qui défend recoit un double dégat
        de la part du pokémon qui attaqeu?
        """
        return ApiPokemon.get_double_damage_from(type_qui_defend, type_qui_attaque)

    @staticmethod
    def get_half_damage_from(type_qui_defend, type_qui_attaque):
        return ApiPokemon.get_half_damage_from(type_qui_defend, type_qui_attaque)

    @staticmethod
    def get_double_damage_to(type_qui_attaque, type_qui_defend):
        return ApiPokemon.get_double_damage_to(type_qui_attaque, type_qui_defend)

    @staticmethod
    def get_half_damage_to(type_qui_attaque, type_qui_defend):
        return ApiPokemon.get_half_damage_to(type_qui_attaque, type_qui_defend)
