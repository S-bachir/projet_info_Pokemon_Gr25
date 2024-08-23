import requests

from metier.pokemon import Pokemon


class ApiPokemon:

    def __init__(self):
        pass

    @staticmethod
    def get_all_pokemons():
        """
        Fait un appel au webservice pour obtenir la liste des pokemons
        accessible.
        :return: La liste des pokemons accessibles
        :rtype: list
        """

        requete1 = requests.get("https://pokeapi.co/api/v2/pokemon/?offset=20&limit=100")
        output_pokemons = []
        if requete1.status_code == 200:
            reponse_json1 = requete1.json()
            for pokemon_json in reponse_json1["results"]:
                requete2 = requests.get("https://pokeapi.co/api/v2/pokemon/" + pokemon_json["name"])
                requete3 = requests.get("https://pokeapi.co/api/v2/pokemon-species/" + pokemon_json["name"])
                if requete2.status_code == 200:
                    reponse_json2 = requete2.json()
                    reponse_json3 = requete3.json()
                    rep_moves = []
                    for moves in reponse_json2["moves"]:
                        move = moves["move"]["name"]
                        requete4 = requests.get("https://pokeapi.co/api/v2/move/" + move)
                        reponse_json4 = requete4.json()["power"]
                        if type(reponse_json4) == int and reponse_json4 > 0:
                            rep_moves.append(move)
                            if len(rep_moves) == 4:
                                break
                            else:
                                continue

                    output_pokemons.append(Pokemon(
                        nom_poke=reponse_json3["names"][4]["name"],
                        id_poke=reponse_json2["id"],
                        niveau_exp=reponse_json2["base_experience"],
                        nom_attaque_1=rep_moves[0],
                        nom_attaque_2=rep_moves[1],
                        nom_attaque_3=rep_moves[2],
                        nom_attaque_4=rep_moves[3],
                        defense=reponse_json2["stats"][2]["base_stat"],
                        vitesse=reponse_json2["stats"][5]["base_stat"],
                        type_poke=reponse_json2["types"][0]["type"]["name"]))

        return output_pokemons

    @staticmethod
    def get_puissance_attaque(name_attaque):
        requete = requests.get("https://pokeapi.co/api/v2/move/" + name_attaque)
        reponse = requete.json()["pp"]
        return reponse

    @staticmethod
    def get_power_attaque(name_attaque):
        requete = requests.get("https://pokeapi.co/api/v2/move/" + name_attaque)
        reponse = requete.json()["power"]
        return reponse

    @staticmethod
    def get_capture_rate(id_pokemon):
        requete = requests.get("https://pokeapi.co/api/v2/pokemon-species/" + str(id_pokemon))
        reponse = requete.json()["capture_rate"]
        return reponse

    @staticmethod
    def get_image_poke(id_poke):
        requete = requests.get(
            "https://pokeres.bastionbot.org/images/pokemon/" + str(id_poke) + ".png", stream=True
        )
        return requete

    @staticmethod
    def get_french_translate_attaque_name(word_to_translate):
        requete = requests.get("https://pokeapi.co/api/v2/move/" + word_to_translate)
        reponse = requete.json()["names"][3]["name"]
        return reponse

    @staticmethod
    def get_french_translate_type_name(type):
        requete = requests.get("https://pokeapi.co/api/v2/type/" + type)
        reponse = requete.json()["names"][2]["name"]

        return reponse

    @staticmethod
    def get_double_damage_from(type_qui_defend, type_qui_attaque):
        """
        Est ce que le pokémoon qui défend recoit un double dégat
        de la part du pokémon qui attaqeu?
        """
        reponse = False
        requete = requests.get("https://pokeapi.co/api/v2/type/" + type_qui_defend)
        liste = requete.json()["damage_relations"]["double_damage_from"]
        for i in liste:
            if i['name'] == type_qui_attaque:
                reponse = True
        return reponse

    @staticmethod
    def get_half_damage_from(type_qui_defend, type_qui_attaque):
        reponse = False
        requete = requests.get("https://pokeapi.co/api/v2/type/" + type_qui_defend)
        liste = requete.json()["damage_relations"]["half_damage_from"]
        for i in liste:
            if i['name'] == type_qui_attaque:
                reponse = True
        return reponse

    @staticmethod
    def get_double_damage_to(type_qui_attaque, type_qui_defend):
        """
        Est ce que le pokémon qui attaque inflige un double dégat
        au pokémon qui défend?
        """
        reponse = False
        requete = requests.get("https://pokeapi.co/api/v2/type/" + type_qui_attaque)
        liste = requete.json()["damage_relations"]["double_damage_to"]

        for i in liste:
            if i['name'] == type_qui_defend:
                reponse = True

        return reponse

    @staticmethod
    def get_half_damage_to(type_qui_attaque, type_qui_defend):

        reponse = False
        requete = requests.get("https://pokeapi.co/api/v2/type/" + type_qui_attaque)
        liste = requete.json()["damage_relations"]["half_damage_to"]

        for i in liste:
            if i['name'] == type_qui_defend:
                reponse = True
        return reponse
