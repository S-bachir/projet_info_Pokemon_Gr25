
class Session:
    def __init__(self):
        """
        Définition des variables que l'on stocke en session
        Le syntaxe
        ref:type = valeur
        permet de donner le type des variables. Utile pour l'autocompletion.
        """
        self.id_dresseur = None
        self.id_utilisateur = None
        self.user_name = None
        self.dresseur_actif = None  # objet dresseur
        self.dresseur_adverse = None
        self.pokemon_actif = None  # objet pokemon
        self.pokemon_adverse = None
        self.adversaire = None  # dresseur ou pokemon sauvage de type string
        self.pokedex = None  # objet pokedex
        self.liste_poke_dresseur = None  # liste d'objet pokemon du dresseur
        self.liste_poke_dresseur_adverse = None  # liste d'objet pokemon du dresseur adverse
