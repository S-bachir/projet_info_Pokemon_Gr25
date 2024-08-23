from webservice.api_pokemon import ApiPokemon


class CapturePokeService:

    def __init__(self):
        pass

    @staticmethod
    def capture_pokemon(pokemon_adverse, name_ball):
        # 100 est le nombre de pv max
        taux_capture = ApiPokemon.get_capture_rate(pokemon_adverse.id_poke)
        if name_ball == "poke-ball":
            a = (1 - (2 / 3) * (pokemon_adverse.pv / 100)) * taux_capture * 1
        elif name_ball == "great-ball":
            a = (1 - (2 / 3) * (pokemon_adverse.pv / 100)) * taux_capture * 1.5
        else:  # ultra-ball
            a = (1 - (2 / 3) * (pokemon_adverse.pv / 100)) * taux_capture * 2

        if a >= 255:
            capture = True
        else:
            from random import randint
            b = 65535 * ((a / 255) ** (1 / 4))
            alea1 = randint(0, 65535)
            alea2 = randint(0, 65535)
            alea3 = randint(0, 65535)
            alea4 = randint(0, 65535)
            if alea1 <= b and alea2 <= b and alea3 <= b and alea4 <= b:
                capture = True
            else:
                capture = False

        return capture
