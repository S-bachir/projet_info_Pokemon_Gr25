from dao.dresseur_renc_dao import DresseurRencontreDao


class DresseurRencontreService:

    def __init__(self):
        pass

    @staticmethod
    def get_id_dresseur_adverse(id_dresseur_user):
        """
        Récupère un pokemon grâce à son nom
        :param id_dresseur_user:
        :type id_dresseur_user:
        :return:
        :rtype:
        """
        return DresseurRencontreDao.find_dresseur_adverse(id_dresseur_user)

    @staticmethod
    def add_dresseurs_rencontre(dresseur_actif, dresseur_adverse):
        return DresseurRencontreDao.create(dresseur_actif, dresseur_adverse)
