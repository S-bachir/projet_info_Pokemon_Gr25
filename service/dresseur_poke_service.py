from dao.dresseur_poke_dao import DresseurPokeDao


class DresseurPokeService:

    def __init__(self):
        pass

    @staticmethod
    def get_id_poke_from_db(id_dresseur):
        """
        Récupère un pokemon grâce à son nom
        :param id_dresseur:
        :type id_dresseur:
        :return:
        :rtype:
        """
        return DresseurPokeDao.find_poke_by_id(id_dresseur)

    @staticmethod
    def add_dresseur_poke_in_bd(dresseur, pokemon):
        return DresseurPokeDao.create(dresseur, pokemon)

    @staticmethod
    def delete_dresseur_poke(dresseur, pokemon):
        return DresseurPokeDao.delete(dresseur, pokemon)

    @staticmethod
    def get_all_poke(id_dresser):
        return DresseurPokeDao.find_all_poke(id_dresser)
