from dao.pokedex_dao import PokedexDao


class PokedexService:

    def __init__(self):
        pass

    @staticmethod
    def add_pokemon_to_pokedex(dresseur, pokedex, C_R):
        return PokedexDao.create(dresseur, pokedex, C_R)

    @staticmethod
    def update_pokemon_in_pokedex(pokedex, pokemon):
        """
        :param pokemon:
        :param pokedex:
        :type pokemon:
        :type pokedex
        :return:
        :rtype:
        """
        return PokedexDao.update(pokedex, pokemon)

    @staticmethod
    def get_all_pokemons_r(dresseur):
        return PokedexDao.find_poke_r(dresseur)

    @staticmethod
    def get_all_pokemons_c(dresseur):
        return PokedexDao.find_poke_c(dresseur)

    @staticmethod
    def get_all_pokedex():
        return PokedexDao.find_all_pokedex()
