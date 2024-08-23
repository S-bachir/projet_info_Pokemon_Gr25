**JEU POKEMON**

Avant de lancer l'application la mise en place d'une base de données et de certains packages est requise.

> 
1. Installation de packages : Les packages dont dépendent notre application se trouve dans le fichier requirements.txt ainsi que la version python compatible (3.6). Pour les installer faudra lancer la commande "pip install -r requirements.txt" dans le terminal.

2. Pour la mise en place de la base de données, 3 fichiers se trouvent dans le répertoire "bdd".
Parmi ces fichiers se trouvent 2 de format sql à copier/coller et exécuter dans un éditeur de requêtes sql et un autre de format python à lancer dans votre IDE. Ces fichiers sont à exécuter dans l'ordre 1,2,3.
La classe permettant la connexion entre l'application et la base de données se trouve dans "dao/pool_connection.py" et vous y trouverez toutes les informations nécessaires à ce sujet. 
> 

Après avoir mise en place tout cela vous pouvez lancer l'application dans votre IDE en passant par le fichier "main.py" se trouvant à la racine du projet ou en lançant dans le terminal la commande "python3 main.py" ou "python.exe main.py" selon votre système d'exploitation.

La classe prise pour la documentation et les tests unitaires est "PokemonDao" se trouvant dans "dao/pokemon_dao.py" et la classe test correspondant se trouve dans "test/test_pokemon_dao.py".



Merci de votre attention!