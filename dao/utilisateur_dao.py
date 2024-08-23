import psycopg2

from dao.abstract_dao import AbstractDao
from dao.pool_connection import PoolConnection


class UtilisateurDao(AbstractDao):

    @staticmethod
    def create(pseudo, mdp):
        """
        Insère une ligne en base avec l'objet en paramètre.
        Retourne l'objet mise à jour avec son id de la base
        """
        connexion = PoolConnection.getConnexion()
        curseur = connexion.cursor()
        try:
            # On envoie au serveur la requête SQL
            curseur.execute(
                "INSERT INTO utilisateur (pseudo_user, mdp_hash)"
                " VALUES (%s, %s) RETURNING pseudo_user;",
                (pseudo, mdp))
            resultat = curseur.fetchone()[0]

            # On enregistre la transaction en base
            connexion.commit()
        except psycopg2.Error as error:
            # la transaction est annulée
            connexion.rollback()
            raise error
        finally:
            curseur.close()
            PoolConnection.putBackConnexion(connexion)

        return resultat

    @staticmethod
    def find_by_name(pseudo):
        """Va chercher une élément de la base grâce à son id et retourne l'objet python associé"""
        connexion = PoolConnection.getConnexion()
        curseur = connexion.cursor()
        try:
            curseur.execute(
                "SELECT *"
                "\n\t FROM utilisateur "
                "\n\t WHERE pseudo_user= %s",
                (pseudo,))
            resultat = curseur.fetchone()

        finally:
            curseur.close()
            PoolConnection.putBackConnexion(connexion)
        return resultat

    @staticmethod
    def find_all_pseudo():
        connexion = PoolConnection.getConnexion()
        curseur = connexion.cursor()
        try:
            curseur.execute(
                "SELECT pseudo_user"
                "\n\t FROM utilisateur "
            )
            resultats = curseur.fetchall()
            users = []
            for pseudo in resultats:
                users.append(pseudo[0])
        finally:
            curseur.close()
            PoolConnection.putBackConnexion(connexion)
        return users

    @staticmethod
    def update(pseudo, mdp):
        """Met à jour la ligne en base de donnée associé à l'objet métier en paramètre"""
        updated = False
        connexion = PoolConnection.getConnexion()
        curseur = connexion.cursor()
        try:
            curseur.execute(
                "UPDATE utilisateur"
                "\n\t SET "
                "\n\t pseudo_user = %s"
                "\n\t mdp_hash = %s",
                (pseudo, mdp))
            if curseur.rowcount > 0:
                updated = True

            # On enregistre la transaction en base
            connexion.commit()
        except psycopg2.Error as error:
            # la transaction est annulée
            connexion.rollback()
            raise error
        finally:
            curseur.close()
            PoolConnection.putBackConnexion(connexion)

        return updated
