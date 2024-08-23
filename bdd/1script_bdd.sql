DROP TABLE IF EXISTS utilisateur CASCADE;
CREATE TABLE utilisateur (
	pseudo_user VARCHAR(10),
	mdp_hash VARCHAR,
	CONSTRAINT pk_pseudo_user PRIMARY KEY(pseudo_user)
);


DROP TABLE IF EXISTS dresseur CASCADE;
CREATE TABLE dresseur(
	id_dresseur INT,
	nom_dresseur VARCHAR(23),
	argent INT,
	pokemon_actif VARCHAR(23),
	pseudo_user VARCHAR,
	CONSTRAINT pk_id_dresseur PRIMARY KEY(id_dresseur),
	CONSTRAINT fk_user_dresseur FOREIGN KEY (pseudo_user) REFERENCES utilisateur(pseudo_user)
);


DROP TABLE IF EXISTS pokemon CASCADE;
CREATE TABLE pokemon(
	id_poke INT,
	nom_poke VARCHAR(23),
	pv INT,
	niveau_exp FLOAT,
	nom_attaque_1 VARCHAR,
	nom_attaque_2 VARCHAR,
	nom_attaque_3 VARCHAR,
	nom_attaque_4 VARCHAR,
	defense INT,
	vitesse  INT,
	type_poke VARCHAR(23),
	CONSTRAINT pk_id_poke PRIMARY KEY (id_poke)
);


DROP TABLE IF EXISTS nn_dresseur_pokemon CASCADE;
CREATE TABLE  nn_dresseur_pokemon(
	id_poke INT,
	id_dresseur INT,
	CONSTRAINT pk_poke_dresseur PRIMARY KEY(id_poke, id_dresseur),
	CONSTRAINT fk_poke_adverse FOREIGN KEY (id_poke) REFERENCES pokemon (id_poke),
	CONSTRAINT fk_dresseur_pokemon FOREIGN KEY (id_dresseur) REFERENCES dresseur(id_dresseur)
);


DROP TABLE IF EXISTS magasin CASCADE;
CREATE TABLE magasin (
	name_ball VARCHAR(25) NOT NULL,
	prix INT,
	CONSTRAINT pk_name_ball_mag PRIMARY KEY (name_ball)
);


DROP TABLE IF EXISTS nn_dresseur_ball CASCADE;
CREATE TABLE nn_dresseur_ball (
	name_ball VARCHAR(25) NOT NULL,
	id_dresseur INT,
	CONSTRAINT pk_dresseur_ball PRIMARY KEY (id_dresseur, name_ball),
	CONSTRAINT fk_dresseur_ball FOREIGN KEY (id_dresseur) REFERENCES dresseur(id_dresseur),
	CONSTRAINT fk_name_ball FOREIGN KEY (name_ball) REFERENCES magasin(name_ball)
);


DROP TABLE IF EXISTS pokedex CASCADE;
CREATE TABLE pokedex(
    id_pokedex SERIAL,
    liste_id_poke VARCHAR,
    id_dresseur INT,
    rencontrer_capturer VARCHAR,
	CONSTRAINT pk_id_pokedex PRIMARY KEY (id_pokedex),
	CONSTRAINT fk_dresseur_pokedex FOREIGN KEY (id_dresseur) REFERENCES dresseur(id_dresseur)
);


DROP TABLE IF EXISTS nn_dresseurs CASCADE;
CREATE TABLE nn_dresseurs(
	id_dresseur_user INT,
	id_dresseur_adverse INT,
	CONSTRAINT pk_dresseur_user_adverse PRIMARY KEY (id_dresseur_user, id_dresseur_adverse),
	CONSTRAINT fk_id_dresseur_user FOREIGN KEY (id_dresseur_user) REFERENCES dresseur(id_dresseur),
	CONSTRAINT fk_id_dresseur_adverse FOREIGN KEY (id_dresseur_adverse) REFERENCES dresseur(id_dresseur)
);
