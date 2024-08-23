from unittest import TestCase

from metier.pokemon import Pokemon
from dao.pokemon_dao import PokemonDao


class TestPokemonDao(TestCase):
    def test_create(self):
        """
        On teste l'insertion d'un pokemon. Puis on supprime la ligne.
        """
        # GIVEN
        pokemon = Pokemon(nom_poke="dugtrio", id_poke=121, niveau_exp=30,
                          nom_attaque_1="scratch", nom_attaque_2="cut",
                          nom_attaque_3="headbutt", nom_attaque_4="wrap",
                          type_poke='grass', defense=40, vitesse=30)

        # WHEN
        new_pokemon = PokemonDao.create(pokemon)
        PokemonDao.delete(new_pokemon)

        # THEN
        self.assertIsInstance(new_pokemon, Pokemon,
                              "n'est pas de la bonne classe")
        self.assertIsNotNone(new_pokemon.id_poke, "aucun identifiant")

    def test_find_by_id(self):
        """
        On crée un pokémon et on l'ajoute dans la base de donnée.
        on cherche ce pokemon via son id dans la base.
        A partir de ce pokémon récupéré, on verifie que c'est bien une instance de la classe Pokemon
        Enfin on vérifie l'égalité des identifiants des pokémons inséré et récupéré.
        """
        # GIVEN
        pokemon = Pokemon(nom_poke="dugtrio", id_poke=121, niveau_exp=30,
                          nom_attaque_1="scratch", nom_attaque_2="cut",
                          nom_attaque_3="headbutt", nom_attaque_4="wrap",
                          type_poke='grass', defense=40, vitesse=30)

        # WHEN
        new_pokemon = PokemonDao.create(pokemon)

        pokemon_db = PokemonDao.find_by_id(new_pokemon.id_poke)
        # On supprime la ligne
        PokemonDao.delete(new_pokemon)

        # THEN
        self.assertIsInstance(pokemon_db, Pokemon,
                              "n'est pas de la bonne classe")
        self.assertEqual(new_pokemon.id_poke, pokemon_db.id_poke,
                         "problème dans les id_poke")

    def test_find_by_name(self):
        """
        on cherche le pokemon qu'on vient d'insérer dans la base via son nom.
        Puis on verifie que c'est bien une instance de la classe Pokemon.
        Enfin on vérifie l'égalité des noms des pokémons inséré et récupéré.
        """

        # GIVEN
        pokemon = Pokemon(nom_poke="dugtrio", id_poke=121, niveau_exp=30,
                          nom_attaque_1="scratch", nom_attaque_2="cut",
                          nom_attaque_3="headbutt", nom_attaque_4="wrap",
                          type_poke='grass', defense=40, vitesse=30)

        # WHEN
        new_pokemon = PokemonDao.create(pokemon)
        pokemon_db = PokemonDao.find_by_name(new_pokemon.nom_poke)

        # On supprime la ligne
        PokemonDao.delete(new_pokemon)

        # THEN
        self.assertIsInstance(pokemon_db, Pokemon,
                              "n'est pas de la bonne classe")
        self.assertEqual(new_pokemon.nom_poke, pokemon_db.nom_poke,
                         "problème dans les nom_poke")

    def test_find_all(self):
        """
        On teste si dans la base de donnée il y a des pokémons.
        """

        # GIVEN
        pokemon = Pokemon(nom_poke="dugtrio", id_poke=121, niveau_exp=30,
                          nom_attaque_1="scratch", nom_attaque_2="cut",
                          nom_attaque_3="headbutt", nom_attaque_4="wrap",
                          type_poke='grass', defense=40, vitesse=30)

        # WHEN
        new_pokemon = PokemonDao.create(pokemon)
        pokemons = PokemonDao.find_all()

        # On supprime la ligne
        PokemonDao.delete(new_pokemon)

        # THEN
        self.assertIsNotNone(pokemons, "aucun pokemon trouvé")

    def test_update(self):
        """
        On teste la mise à jour en vérifiant qu'on met à jour
        la ligne qu'on vient d'insérer. Puis on le supprime
        """

        # GIVEN
        pokemon = Pokemon(nom_poke="dugtrio", id_poke=121, niveau_exp=30,
                          nom_attaque_1="scratch", nom_attaque_2="cut",
                          nom_attaque_3="headbutt", nom_attaque_4="wrap",
                          type_poke='grass', defense=40, vitesse=30)

        PokemonDao.create(pokemon)

        pokemon_update = Pokemon(nom_poke="dugtrio", id_poke=121, niveau_exp=50,
                                 nom_attaque_1="fire-punch", nom_attaque_2="cut",
                                 nom_attaque_3="double-kick", nom_attaque_4="tackle",
                                 type_poke='poison', defense=80, vitesse=100)

        # WHEN
        updated = PokemonDao.update(pokemon_update)
        PokemonDao.delete(pokemon_update)

        # THEN
        self.assertTrue(updated)

    def test_delete(self):
        """
        On teste la suppression en verifiant que l'on supprime bien la ligne
        que l'on vient d'insérer.
        """
        # GIVEN
        pokemon = Pokemon(nom_poke="dugtrio", id_poke=121, niveau_exp=30,
                          nom_attaque_1="scratch", nom_attaque_2="cut",
                          nom_attaque_3="headbutt", nom_attaque_4="wrap",
                          type_poke='grass', defense=40, vitesse=30)
        # WHEN
        new_pokemon = PokemonDao.create(pokemon)
        deleted = PokemonDao.delete(new_pokemon)

        # THEN
        self.assertTrue(deleted)
