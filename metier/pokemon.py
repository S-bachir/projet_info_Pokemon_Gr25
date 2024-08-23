

class Pokemon:
    NOM_BASE_DE_DONNEE = "pokemon"

    def __init__(self, nom_poke, id_poke, niveau_exp, nom_attaque_1, nom_attaque_2,
                 nom_attaque_3, nom_attaque_4, type_poke, defense, vitesse, pv=100):

        self.nom_poke = nom_poke
        self.id_poke = id_poke
        self.type_poke = type_poke
        self.niveau_exp = niveau_exp
        self.nom_attaque_1 = nom_attaque_1
        self.nom_attaque_2 = nom_attaque_2
        self.nom_attaque_3 = nom_attaque_3
        self.nom_attaque_4 = nom_attaque_4
        self.defense = defense
        self.vitesse = vitesse
        self.pv = pv
        self.description_defense = "Défense du pokemon "+self.nom_poke+" d'une capacité de "+str(self.defense)+" points"
        self.data_base_pokemon = Pokemon.NOM_BASE_DE_DONNEE

        if self.pv < 0:
            self.pv=0
