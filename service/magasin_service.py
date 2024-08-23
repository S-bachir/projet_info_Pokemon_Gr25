from dao.magasin_dao import MagasinDao
from time_print import delay_print


class MagasinService:

    def __init__(self):
        pass

    @staticmethod
    def acheter_ball(dresseur, ball):
        boolean = False
        if dresseur.argent >= ball.prix:
            boolean = True

        else:
            pass

        return boolean

    @staticmethod
    def get_ball_from_db_by_name(name_ball):
        """
        Récupère un pokemon grâce à son nom
        :param name_ball:
        :type name_ball:
        :return:
        :rtype:
        """
        return MagasinDao.find_by_name(name_ball)

    @staticmethod
    def get_all_balls_from_db():
        return MagasinDao.find_all()

    @staticmethod
    def add_ball_to_db(ball):
        """

        :param ball:
        :type ball:
        :return:
        :rtype:
        """

        return MagasinDao.create(ball)
