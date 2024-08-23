import psycopg2

from dao.abstract_dao import AbstractDao
from dao.pool_connection import PoolConnection
from metier.dresseur import Dresseur


class DresseurDao(AbstractDao):

    @staticmethod
    def create(dresseur):
        """Insère une ligne en base avec l'objet en paramètre. Retourne l'objet mise à jour avec son id de la base"""
        connexion = PoolConnection.getConnexion()
        curseur = connexion.cursor()
        try:
            # On envoie au serveur la requête SQL
            curseur.execute(
                "INSERT INTO dresseur (id_dresseur, nom_dresseur, argent,"
                " pokemon_actif)"
                " VALUES (%s, %s, %s, %s) RETURNING id_dresseur;",
                (dresseur.id_dresseur,
                 dresseur.nom_dresseur,
                 dresseur.argent,
                 dresseur.pokemon_actif))
            dresseur.id_dresseur = curseur.fetchone()[0]

            # On enregistre la transaction en base
            connexion.commit()
        except psycopg2.Error as error:
            # la transaction est annulée
            connexion.rollback()
            raise error
        finally:
            curseur.close()
            PoolConnection.putBackConnexion(connexion)

        return dresseur

    @staticmethod
    def find_by_id(id):
        """Va chercher une élément de la base grâce à son id et retourne l'objet python associé"""
        connexion = PoolConnection.getConnexion()
        curseur = connexion.cursor()
        try:
            curseur.execute(
                "SELECT id_dresseur, nom_dresseur, argent,"
                "pokemon_actif, pseudo_user"
                "\n\t FROM dresseur"
                "\n\t WHERE id_dresseur= %s",
                (id,))
            resultat = curseur.fetchone()
            dresseur = None
            # Si on a un résultat
            if resultat:
                dresseur = Dresseur(
                    id_dresseur=resultat[0],
                    nom_dresseur=resultat[1],
                    argent=resultat[2],
                    pokemon_actif=resultat[3],
                    pseudo_user=resultat[4])
                # A compléter au cas où
        finally:
            curseur.close()
            PoolConnection.putBackConnexion(connexion)
        return dresseur

    @staticmethod
    def find_by_name(name):
        """Va chercher une élément de la base grâce à son id et retourne l'objet python associé"""
        connexion = PoolConnection.getConnexion()
        curseur = connexion.cursor()
        try:
            curseur.execute(
                "SELECT id_dresseur, nom_dresseur, argent, pokemon_actif, pseudo_user"
                "\n\t FROM dresseur"
                "\n\t WHERE nom_dresseur= %s",
                (name,))
            resultat = curseur.fetchone()
            dresseur = None
            # Si on a un résultat
            if resultat:
                dresseur = Dresseur(
                    id_dresseur=resultat[0],
                    nom_dresseur=resultat[1],
                    argent=resultat[2],
                    pokemon_actif=resultat[3],
                    pseudo_user=resultat[4])
                # A compléter au cas où
        finally:
            curseur.close()
            PoolConnection.putBackConnexion(connexion)
        return dresseur

    @staticmethod
    def find_all():
        """Retourne tous les éléments d'une table sous forme de liste d'objets python"""
        connexion = PoolConnection.getConnexion()
        curseur = connexion.cursor()
        try:
            curseur.execute(
                "SELECT id_dresseur, nom_dresseur, argent,"
                "pokemon_actif, pseudo_user"
                "\n\t FROM dresseur"
            )
            resultats = curseur.fetchall()
            dresseurs = []
            for resultat in resultats:
                dresseurs.append(
                    Dresseur(
                        id_dresseur=resultat[0],
                        nom_dresseur=resultat[1],
                        argent=resultat[2],
                        pokemon_actif=resultat[3],
                        pseudo_user=resultat[4])
                )
        finally:
            curseur.close()
            PoolConnection.putBackConnexion(connexion)
        return dresseurs

    @staticmethod
    def find_all_none_user():
        """Retourne tous les éléments d'une table sous forme de liste d'objets python"""
        connexion = PoolConnection.getConnexion()
        curseur = connexion.cursor()
        try:
            curseur.execute(
                "SELECT id_dresseur, nom_dresseur, argent,"
                "pokemon_actif, pseudo_user"
                "\n\t FROM dresseur"
                "\n\t WHERE pseudo_user is NULL"
            )
            resultats = curseur.fetchall()
            dresseurs = []
            for resultat in resultats:
                dresseurs.append(
                    Dresseur(
                        id_dresseur=resultat[0],
                        nom_dresseur=resultat[1],
                        argent=resultat[2],
                        pokemon_actif=resultat[3],
                        pseudo_user=resultat[4])
                )
        finally:
            curseur.close()
            PoolConnection.putBackConnexion(connexion)
        return dresseurs

    @staticmethod
    def update(dresseur):
        """Met à jour la ligne en base de donnée associé à l'objet métier en paramètre"""
        updated = False
        connexion = PoolConnection.getConnexion()
        curseur = connexion.cursor()
        try:
            curseur.execute(
                "UPDATE dresseur"
                "\n\tSET "
                "\n\t nom_dresseur = %s"
                "\n\t, argent = %s"
                "\n\t, pokemon_actif = %s"
                "\n\t, pseudo_user = %s"
                "\n\t WHERE id_dresseur= %s",
                (dresseur.nom_dresseur,
                 dresseur.argent,
                 dresseur.pokemon_actif,
                 dresseur.pseudo_user,
                 dresseur.id_dresseur))

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
                "DELETE FROM dresseur WHERE id_dresseur=%s;",
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

    @staticmethod
    def find_dresseur_by_user(pseudo_user):
        connexion = PoolConnection.getConnexion()
        curseur = connexion.cursor()
        try:
            curseur.execute(
                "SELECT id_dresseur, nom_dresseur, argent,"
                "pokemon_actif, pseudo_user"
                "\n\t FROM dresseur"
                "\n\t WHERE pseudo_user = %s",
                (pseudo_user,))
            resultat = curseur.fetchone()
            dresseur = None
            # Si on a un résultat
            if resultat:
                dresseur = Dresseur(
                    id_dresseur=resultat[0],
                    nom_dresseur=resultat[1],
                    argent=resultat[2],
                    pokemon_actif=resultat[3],
                    pseudo_user=pseudo_user)
                # A compléter au cas où
        finally:
            curseur.close()
            PoolConnection.putBackConnexion(connexion)
        return dresseur
