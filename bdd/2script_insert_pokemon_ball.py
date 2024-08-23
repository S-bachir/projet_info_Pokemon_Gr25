from service.pokemon_service import PokemonService
from service.magasin_service import MagasinService
from webservice.api_pokemon import ApiPokemon
from webservice.api_ball import ApiBall

balls = ApiBall.get_ball()
for ball in balls:
    MagasinService.add_ball_to_db(ball)

pokemons = ApiPokemon.get_all_pokemons()
for pokemon in pokemons:
    PokemonService.add_pokemon_to_db(pokemon)
