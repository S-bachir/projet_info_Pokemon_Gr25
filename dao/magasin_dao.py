import psycopg2

from dao.abstract_dao import AbstractDao
from dao.pool_connection import PoolConnection
from metier.magasin_ball import Ball


class MagasinDao(AbstractDao):

    @staticmethod
    def create(ball):
        """Insère une ligne en base avec l'objet en paramètre. Retourne l'objet mise à jour avec son id de la base"""
        connexion = PoolConnection.getConnexion()
        curseur = connexion.cursor()
        try:
            # On envoie au serveur la requête SQL
            curseur.execute(
                "INSERT INTO magasin (name_ball, prix)"
                " VALUES (%s, %s) RETURNING name_ball;",
                (ball.name_ball,
                 ball.prix))
            ball.name_ball = curseur.fetchone()[0]

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
    def find_by_name(name_ball):
        """Va chercher une élément de la base grâce à son id et retourne l'objet python associé"""
        connexion = PoolConnection.getConnexion()
        curseur = connexion.cursor()
        try:
            curseur.execute(
                "SELECT name_ball, prix"
                "\n\t FROM magasin "
                "\n\t WHERE name_ball= %s",
                (name_ball,))
            resultat = curseur.fetchone()
            ball = None
            # Si on a un résultat
            if resultat:
                ball = Ball(
                    name_ball=resultat[0],
                    prix=resultat[1])

        finally:
            curseur.close()
            PoolConnection.putBackConnexion(connexion)
        return ball

    @staticmethod
    def find_all():
        """Retourne tous les éléments d'une table sous forme de liste d'objets python"""
        connexion = PoolConnection.getConnexion()
        curseur = connexion.cursor()
        try:
            curseur.execute(
                "SELECT *"
                "\n\t FROM magasin"
            )
            resultats = curseur.fetchall()
            balls = []
            for resultat in resultats:
                balls.append(
                    Ball(
                        name_ball=resultat[0],
                        prix=resultat[1])
                )
        finally:
            curseur.close()
            PoolConnection.putBackConnexion(connexion)

        return balls
