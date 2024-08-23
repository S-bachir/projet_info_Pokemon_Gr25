from dao.utilisateur_dao import UtilisateurDao


class UtilisateurService:

    def __init__(self):
        pass

    @staticmethod
    def add_user_in_db(pseudo, mdp):
        return UtilisateurDao.create(pseudo, mdp)

    @staticmethod
    def get_user_by_name(pseudo):
        return UtilisateurDao.find_by_name(pseudo)

    @staticmethod
    def update_info_user(pseudo, mdp):
        return UtilisateurDao.update(pseudo, mdp)

    @staticmethod
    def get_all_user():
        return UtilisateurDao.find_all_pseudo()
