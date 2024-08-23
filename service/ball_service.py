
from dao.ball_dao import BallDao


class BallService:

    def __init__(self):
        pass

    @staticmethod
    def add_ball_in_db(dresseur, ball):
        return BallDao.create(dresseur, ball)

    @staticmethod
    def get_ball(ball):
        return BallDao.find_by_name(ball)

    @staticmethod
    def get_all_balls_from_db(id_dresseur):
        return BallDao.find_ball_by_id(id_dresseur)

    @staticmethod
    def delete_ball_from_db(name_ball):
        return BallDao.delete(name_ball)
