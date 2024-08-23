import psycopg2
from psycopg2 import pool

host = "localhost"
port = "5432"
database = "pokemon"
user = "admin"
password = "admin"


class PoolConnection:
    """
    Cette classe va gérer la connexion à la base de données.

    Son fonctionnement est un peu particulier car c'est une classe singleton.
    Tous les objets ReservoirConnexion que vous allez instancier vont faire
    référence au même objet. Ainsi on s'assure de ne pas créer plus de
    connexions que nécessaire.

    Si vous voulez une connexion faite simplement appel à la méthode
    getConnexion. Cette méthode va instacier les connexion si nécessaire et
    vous en renvoyer une.
    """

    __instance = None

    @staticmethod
    def getInstance():
        """
        C'est la méthode que l'on va utiliser si l'on veut obtenir l'instance
        de de ReservoirConnexion
        :return: le singleton ReservoirConnexion
        :rtype: PoolConnection
        """
        if PoolConnection.__instance is None:
            PoolConnection()
        return PoolConnection.__instance

    @staticmethod
    def getConnexion():
        """
        Méthode qui retourne une connexion utilisable
        :return: une connexion à la base
        """
        return PoolConnection.getInstance().getconn()

    @staticmethod
    def closeConnexions():
        """
        Ferme toutes les connexions ouvertes
        :return: si les connexions ont pu être fermées.
        :rtype: bool
        """
        try:
            PoolConnection.getInstance().closeall()
            closed = True
        except Exception:
            print("Problème lors de la fermeture")
            closed = False
        return closed

    @staticmethod
    def putBackConnexion(connection):
        PoolConnection.getInstance().putconn(connection)

    def __init__(self):
        """
        Constructeur de notre classe. Il est théoriquement privé (non
        utilisable depuis une autre classe). Malheureusement ce n'est pas
        possible en python. À la place on ve lever une exception. Vous ne devez
        pas appeler ce constructeur !
        """
        if PoolConnection.__instance is not None:
            raise Exception("Cette classe est un singleton. Utiliser la "
                            "méthode getInstance()")
        else:
            PoolConnection.__instance = psycopg2.pool.SimpleConnectionPool(1, 2,
                                                                           host=host,
                                                                           port=port,
                                                                           database=database,
                                                                           user=user,
                                                                           password=password,
                                                                           )
