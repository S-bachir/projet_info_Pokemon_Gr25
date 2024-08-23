import psycopg2

from dao.abstract_dao import AbstractDao
from dao.pool_connection import PoolConnection
from metier.pokemon import Pokemon


class PokemonDao(AbstractDao):

    @staticmethod
    def create(pokemon):
        """
        Méthode permettant d'ajouter un pokémon dans notre base de données.

        :param pokemon: l'objet python associé à un pokémon à ajouter
        :type pokemon: Pokemon
        :return: l'objet python associé à un pokémon
        :rtype: Pokemon
        """
        connexion = PoolConnection.getConnexion()
        curseur = connexion.cursor()
        try:
            # On envoie au serveur la requête SQL
            curseur.execute(
                "INSERT INTO pokemon (id_poke, nom_poke, pv,"
                "niveau_exp, nom_attaque_1, nom_attaque_2, nom_attaque_3,"
                "nom_attaque_4, defense,vitesse, type_poke)"
                " VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s) RETURNING id_poke;",
                (pokemon.id_poke,
                 pokemon.nom_poke,
                 pokemon.pv,
                 pokemon.niveau_exp,
                 pokemon.nom_attaque_1,
                 pokemon.nom_attaque_2,
                 pokemon.nom_attaque_3,
                 pokemon.nom_attaque_4,
                 pokemon.defense,
                 pokemon.vitesse,
                 pokemon.type_poke))
            # On récupère l'id généré
            pokemon.id_poke = curseur.fetchone()[0]

            # On enregistre la transaction en base
            connexion.commit()
        except psycopg2.Error as error:
            # la transaction est annulée
            connexion.rollback()
            raise error
        finally:
            curseur.close()
            PoolConnection.putBackConnexion(connexion)

        return pokemon

    @staticmethod
    def find_by_id(id):
        """
        Méthode permettant de chercher un pokémon grâce à son id et retourne l'objet python associé

        :param id: l'identifiant du pokemon recherché
        :type id: int
        :return: l'objet python associé à un pokémon
        :rtype: Pokemon
        """
        connexion = PoolConnection.getConnexion()
        curseur = connexion.cursor()
        try:
            curseur.execute(
                "SELECT *"
                "\n\t FROM pokemon "
                "\n\t WHERE id_poke= %s",
                (id,))
            resultat = curseur.fetchone()
            pokemon = None
            # Si on a un résultat

            if resultat:
                pokemon = Pokemon(
                    id_poke=resultat[0],
                    nom_poke=resultat[1],
                    pv=resultat[2],
                    niveau_exp=resultat[3],
                    nom_attaque_1=resultat[4],
                    nom_attaque_2=resultat[5],
                    nom_attaque_3=resultat[6],
                    nom_attaque_4=resultat[7],
                    defense=resultat[8],
                    vitesse=resultat[9],
                    type_poke=resultat[10])

        finally:
            curseur.close()
            PoolConnection.putBackConnexion(connexion)
        return pokemon

    @staticmethod
    def find_by_name(name):
        """
        Méthode permettant de chercher un pokémon grâce à son nom et retourne l'objet python associé

        :param name: le nom du pokémon recherché
        :type name: str
        :return: l'objet python associé à un pokémon
        :rtype: Pokemon
        """
        connexion = PoolConnection.getConnexion()
        curseur = connexion.cursor()
        try:
            curseur.execute(
                "SELECT *"
                "\n\t FROM pokemon "
                "\n\t WHERE nom_poke= %s",
                (name,))
            resultat = curseur.fetchone()
            pokemon = None
            # Si on a un résultat

            if resultat:
                pokemon = Pokemon(
                    id_poke=resultat[0],
                    nom_poke=resultat[1],
                    pv=resultat[2],
                    niveau_exp=resultat[3],
                    nom_attaque_1=resultat[4],
                    nom_attaque_2=resultat[5],
                    nom_attaque_3=resultat[6],
                    nom_attaque_4=resultat[7],
                    defense=resultat[8],
                    vitesse=resultat[9],
                    type_poke=resultat[10])

        finally:
            curseur.close()
            PoolConnection.putBackConnexion(connexion)
        return pokemon

    @staticmethod
    def find_all():
        """
        Méthode permettant de chercher tous les pokémons présents dans une base de donnée

        :return: tous les pokémons d'une table sous forme de liste d'objets python associé
        :rtype: list
        """
        connexion = PoolConnection.getConnexion()
        curseur = connexion.cursor()
        try:
            curseur.execute(
                "SELECT *"
                "\n\t FROM pokemon"
            )
            resultats = curseur.fetchall()
            pokemons = []
            for resultat in resultats:
                pokemons.append(
                    Pokemon(
                        id_poke=resultat[0],
                        nom_poke=resultat[1],
                        pv=resultat[2],
                        niveau_exp=resultat[3],
                        nom_attaque_1=resultat[4],
                        nom_attaque_2=resultat[5],
                        nom_attaque_3=resultat[6],
                        nom_attaque_4=resultat[7],
                        defense=resultat[8],
                        vitesse=resultat[9],
                        type_poke=resultat[10])
                )
        finally:
            curseur.close()
            PoolConnection.putBackConnexion(connexion)
        return pokemons

    @staticmethod
    def update(pokemon):
        """
        Méthode permettant de mettre à jour les informations d'un pokémon dans la base

        :param pokemon: l'objet python associé à un pokémon à mettre à jour
        :type pokemon: Pokemon
        :return: une variable booléenne : True si le pokémon est mis à jour, False sinon
        :rtype: bool
        """
        updated = False
        connexion = PoolConnection.getConnexion()
        curseur = connexion.cursor()
        try:
            curseur.execute(
                "UPDATE pokemon"
                "\n\t SET "
                "\n\t nom_poke = %s"
                "\n\t, niveau_exp = %s"
                "\n\t, nom_attaque_1 = %s"
                "\n\t, nom_attaque_2 = %s"
                "\n\t, nom_attaque_3 = %s"
                "\n\t, nom_attaque_4 = %s"
                "\n\t, defense = %s"
                "\n\t, vitesse = %s"
                "\n\t, type_poke = %s"
                "\n\t WHERE id_poke= %s",
                (pokemon.nom_poke,
                 pokemon.niveau_exp,
                 pokemon.nom_attaque_1,
                 pokemon.nom_attaque_2,
                 pokemon.nom_attaque_3,
                 pokemon.nom_attaque_4,
                 pokemon.defense,
                 pokemon.vitesse,
                 pokemon.type_poke,
                 pokemon.id_poke))
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
    def delete(pokemon):
        """
        Méthode permettant de supprimer un pokémon dans la base

        :param pokemon: l'objet python associé à un pokémon à supprimer
        :type pokemon: Pokemon
        :return: une variable booléenne : True si le pokémon est supprimer, False sinon
        :rtype: bool
        """
        deleted = False
        connexion = PoolConnection.getConnexion()
        curseur = connexion.cursor()
        try:
            # On envoie au serveur la requête SQL
            curseur.execute(
                "DELETE FROM pokemon WHERE id_poke=%s;",
                (pokemon.id_poke,))

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
