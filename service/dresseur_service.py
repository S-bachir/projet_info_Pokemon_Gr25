
from dao.dresseur_dao import DresseurDao


class DresseurService:
    """
    DresseurService va manipuler les dresseurs pour qu'ils agissent. Toutes
    les méthodes de la classe sont statiques car DresseurService n'a pas
    d'état. Il va seulement manipuler les dresseurs qu'on lui passe en
    paramètre de ces fonctions.
    """

    def __init__(self):
        pass

    @staticmethod
    def get_all_dresseurs_from_db():
        return DresseurDao.find_all()

    @staticmethod
    def get_all_dresseurs_none_user():
        return DresseurDao.find_all_none_user()

    @staticmethod
    def get_id_dresseur_by_name(name_dresseur):
        return DresseurDao.find_by_name(name_dresseur)

    @staticmethod
    def update_dresseur_in_db(dresseur):
        return DresseurDao.update(dresseur)

    @staticmethod
    def get_dresseur_by_id(id_dresseur):
        return DresseurDao.find_by_id(id_dresseur)

    @staticmethod
    def get_dresseur_by_user(pseudo_user):
        return DresseurDao.find_dresseur_by_user(pseudo_user)
