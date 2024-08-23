import psycopg2

from dao.abstract_dao import AbstractDao
from dao.pool_connection import PoolConnection
from metier.magasin_ball import Ball


class BallDao(AbstractDao):

    @staticmethod
    def create(dresseur, ball):
        """
        Insère une ligne en base avec l'objet en paramètre.
        Retourne l'objet mise à jour avec son id de la base
        """
        connexion = PoolConnection.getConnexion()
        curseur = connexion.cursor()
        try:
            # On envoie au serveur la requête SQL
            curseur.execute(
                "INSERT INTO nn_dresseur_ball (id_dresseur, name_ball)"
                " VALUES (%s, %s);",
                (dresseur.id_dresseur, ball.name_ball))

            # On enregistre la transaction en base
            connexion.commit()
        except psycopg2.Error as error:
            # la transaction est annulée
            connexion.rollback()
            raise error
        finally:
            curseur.close()
            PoolConnection.putBackConnexion(connexion)

        return ball

    @staticmethod
    def find_ball_by_id(id_dresseur):
        """
        Va chercher une élément de la base grâce à son id et retourne l'objet python associé
        """
        connexion = PoolConnection.getConnexion()
        curseur = connexion.cursor()
        try:
            curseur.execute(
                "SELECT name_ball"
                "\n\t FROM nn_dresseur_ball "
                "\n\t WHERE id_dresseur= %s",
                (id_dresseur,))
            resultats = curseur.fetchall()
            balls = []
            for resultat in resultats:
                balls.append(
                    resultat[0]
                )
        finally:
            curseur.close()
            PoolConnection.putBackConnexion(connexion)
        return balls

    @staticmethod
    def delete(dresseur):
        """
        Supprime la ligne en base représentant l'objet en paramètre
        :return si une supression à eu lieu
        :rtype bool
        """
        deleted = False
        connexion = PoolConnection.getConnexion()
        curseur = connexion.cursor()
        try:
            # On envoie au serveur la requête SQL
            curseur.execute(
                "DELETE FROM nn_dresseur_ball WHERE id_dresseur=%s;",
                (dresseur.id_dresseur,))

            # on verifie s'il y a eu des supressions
            if curseur.rowcount > 0:
                deleted = True

            # On enregistre la transaction en base
            connexion.commit()
        except psycopg2.Error as error:
            # la transaction est annulée
            connexion.rollback()
            raise error
        finally:
            curseur.close()
            PoolConnection.putBackConnexion(connexion)

        return deleted
