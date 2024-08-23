from abc import ABC


class AbstractDao(ABC):

    @staticmethod
    def create(objet_metier):
        """Insère une ligne en base avec l'objet en paramètre. Retourne l'objet mise à jour avec son id de la base"""
        return NotImplementedError

    @staticmethod
    def find_by_id(id):
        """Va chercher une élément de la base grâce à son id et retourne l'objet python associé"""
        return NotImplementedError

    @staticmethod
    def find_all():
        """Retourne tous les éléments d'une table sous forme de liste d'objets python"""
        return NotImplementedError

    @staticmethod
    def update(objet_metier):
        """Met à jour la ligne en base de donnée associé à l'objet métier en paramètre"""
        return NotImplementedError

    @staticmethod
    def delete(objet_metier):
        """
        Supprime la ligne en base représentant l'objet en paramètre
        :return si une supression à eu lieu
        :rtype bool
        """
        return NotImplementedError
