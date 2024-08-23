import psycopg2

from dao.abstract_dao import AbstractDao
from dao.pool_connection import PoolConnection


class DresseurPokeDao(AbstractDao):

    @staticmethod
    def find_poke_by_id(id_dresseur):
        """Va chercher une élément de la base grâce à son id et retourne l'objet python associé"""
        connexion = PoolConnection.getConnexion()
        curseur = connexion.cursor()
        try:
            curseur.execute(
                "SELECT id_poke"
                "\n\t FROM nn_dresseur_pokemon "
                "\n\t WHERE id_dresseur= %s",
                (id_dresseur,))
            resultat = curseur.fetchall()

        finally:
            curseur.close()
            PoolConnection.putBackConnexion(connexion)
        return resultat

    @staticmethod
    def find_all_poke(id_dresser):
        connexion = PoolConnection.getConnexion()
        curseur = connexion.cursor()
        try:
            curseur.execute(
                "SELECT id_poke"
                "\n\t FROM nn_dresseur_pokemon"
                "\n\t WHERE id_dresseur= %s",
                (id_dresser,)
            )
            resultats = curseur.fetchall()
            ids_poke = []
            for resultat in resultats:
                ids_poke.append(resultat[0])
        finally:
            curseur.close()
            PoolConnection.putBackConnexion(connexion)
        return ids_poke

    @staticmethod
    def find_dresseur_by_id(id_poke):
        """Va chercher une élément de la base grâce à son id et retourne l'objet python associé"""
        connexion = PoolConnection.getConnexion()
        curseur = connexion.cursor()
        try:
            curseur.execute(
                "SELECT id_dresseur"
                "\n\t FROM nn_dresseur_pokemon"
                "\n\t WHERE id_poke= %s",
                (id_poke,))
            resultat = curseur.fetchone()[0]

        finally:
            curseur.close()
            PoolConnection.putBackConnexion(connexion)
        return resultat

    @staticmethod
    def create(dresseur, pokemon):
        connexion = PoolConnection.getConnexion()
        curseur = connexion.cursor()
        try:
            # On envoie au serveur la requête SQL
            curseur.execute(
                "INSERT INTO nn_dresseur_pokemon (id_dresseur, id_poke)"
                " VALUES (%s, %s);",
                (dresseur.id_dresseur,
                 pokemon.id_poke))

            # On enregistre la transaction en base
            connexion.commit()
        except psycopg2.Error as error:
            # la transaction est annulée
            connexion.rollback()
            raise error
        finally:
            curseur.close()
            PoolConnection.putBackConnexion(connexion)

        return dresseur, pokemon

    @staticmethod
    def delete(dresseur, pokemon):
        deleted = False
        connexion = PoolConnection.getConnexion()
        curseur = connexion.cursor()
        try:
            # On envoie au serveur la requête SQL
            curseur.execute(
                "DELETE FROM nn_dresseur_pokemon WHERE id_dresseur = %s AND id_poke=%s;",
                (dresseur.id_dresseur, pokemon.id_poke))

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
