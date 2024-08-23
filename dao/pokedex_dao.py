import psycopg2

from dao.abstract_dao import AbstractDao
from dao.pool_connection import PoolConnection
from metier.pokedex import Pokedex


class PokedexDao(AbstractDao):

    @staticmethod
    def create(dresseur, pokedex, C_R):

        connexion = PoolConnection.getConnexion()
        curseur = connexion.cursor()
        try:
            # On envoie au serveur la requête SQL
            curseur.execute(
                "INSERT INTO pokedex (id_dresseur, liste_id_poke, rencontrer_capturer)"
                " VALUES (%s, %s, %s) RETURNING id_pokedex;",
                (dresseur.id_dresseur,
                 pokedex.liste_id_poke,
                 C_R))
            pokedex.id_pokedex = curseur.fetchone()[0]

            # On enregistre la transaction en base
            connexion.commit()
        except psycopg2.Error as error:
            # la transaction est annulée
            connexion.rollback()
            raise error
        finally:
            curseur.close()
            PoolConnection.putBackConnexion(connexion)

        return pokedex

    @staticmethod
    def update(pokedex, pokemon):
        """Met à jour la ligne en base de donnée associé à l'objet métier en paramètre"""
        updated = False
        connexion = PoolConnection.getConnexion()
        curseur = connexion.cursor()

        try:
            curseur.execute(
                "UPDATE pokedex"
                "\n\tSET "
                "\n\t liste_id_poke = %s"
                "\n\t WHERE id_pokedex= %s",
                (pokedex.liste_id_poke + "{},".format(pokemon.id_poke),
                 pokedex.id_pokedex))

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

    @staticmethod
    def find_poke_r(dresseur):
        """Va chercher une élément de la base grâce à son id et retourne l'objet python associé"""
        connexion = PoolConnection.getConnexion()
        curseur = connexion.cursor()
        try:
            curseur.execute(
                "SELECT id_pokedex, liste_id_poke"
                "\n\t FROM pokedex "
                "\n\t WHERE id_dresseur= %s AND rencontrer_capturer = %s",
                (dresseur.id_dresseur, "R",))
            resultat = curseur.fetchone()
            pokedex = None
            # Si on a un résultat

            if resultat:
                pokedex = Pokedex(
                    id_pokedex=resultat[0],
                    liste_id_poke=resultat[1]
                )

        finally:
            curseur.close()
            PoolConnection.putBackConnexion(connexion)
        return pokedex

    @staticmethod
    def find_poke_c(dresseur):
        """Va chercher une élément de la base grâce à son id et retourne l'objet python associé"""
        connexion = PoolConnection.getConnexion()
        curseur = connexion.cursor()
        try:
            curseur.execute(
                "SELECT id_pokedex, liste_id_poke"
                "\n\t FROM pokedex "
                "\n\t WHERE id_dresseur= %s AND rencontrer_capturer = %s",
                (dresseur.id_dresseur, "C",))
            resultat = curseur.fetchone()
            pokedex = None
            # Si on a un résultat

            if resultat:
                pokedex = Pokedex(
                    id_pokedex=resultat[0],
                    liste_id_poke=resultat[1]
                )

        finally:
            curseur.close()
            PoolConnection.putBackConnexion(connexion)
        return pokedex

    @staticmethod
    def find_all_pokedex():
        """Retourne tous les éléments d'une table sous forme de liste d'objets python"""
        connexion = PoolConnection.getConnexion()
        curseur = connexion.cursor()
        try:
            curseur.execute(
                "SELECT id_dresseur, rencontrer_capturer"
                "\n\t FROM pokedex"

            )
            resultats = curseur.fetchall()
        finally:
            curseur.close()
            PoolConnection.putBackConnexion(connexion)
        return resultats
