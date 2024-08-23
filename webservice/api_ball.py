import requests

from metier.magasin_ball import Ball


class ApiBall:

    def __init__(self):
        pass

    @staticmethod
    def get_ball():
        requete1 = requests.get("https://pokeapi.co/api/v2/item/?offset=1&limit=3")
        output_ball = []
        if requete1.status_code == 200:
            reponse_json1 = requete1.json()
            for ball in reponse_json1["results"]:
                requete2 = requests.get("https://pokeapi.co/api/v2/item/" + ball["name"])
                if requete2.status_code == 200:
                    reponse_json2 = requete2.json()
                    output_ball.append(Ball(
                        name_ball=reponse_json2["names"][3]["name"],
                        prix=reponse_json2["cost"]))

        return output_ball
