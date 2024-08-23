import psycopg2

from dao.abstract_dao import AbstractDao
from dao.pool_connection import PoolConnection


class DresseurRencontreDao(AbstractDao):

    @staticmethod
    def create(dresseur_actif, dresseur_adverse):
        connexion = PoolConnection.getConnexion()
        curseur = connexion.cursor()
        try:
            # On envoie au serveur la requête SQL
            curseur.execute(
                "INSERT INTO nn_dresseurs (id_dresseur_user, id_dresseur_adverse)"
                " VALUES (%s, %s);",
                (dresseur_actif.id_dresseur,
                 dresseur_adverse.id_dresseur))

            # On enregistre la transaction en base
            connexion.commit()
        except psycopg2.Error as error:
            # la transaction est annulée
            connexion.rollback()
            raise error
        finally:
            curseur.close()
            PoolConnection.putBackConnexion(connexion)

        return dresseur_actif, dresseur_adverse

    @staticmethod
    def find_dresseur_adverse(id_dresseur_user):
        connexion = PoolConnection.getConnexion()
        curseur = connexion.cursor()
        try:
            curseur.execute(
                "SELECT id_dresseur_adverse"
                "\n\t FROM nn_dresseurs"
                "\n\t WHERE id_dresseur_user= %s",
                (id_dresseur_user,))
            resultat = curseur.fetchall()

        finally:
            curseur.close()
            PoolConnection.putBackConnexion(connexion)
        return resultat
