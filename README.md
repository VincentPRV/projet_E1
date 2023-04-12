# Projet E1 - README

## Description

Ce projet a pour but de créer une base de données permettant de stocker des informations sur des auteurs et leurs oeuvres, ainsi que sur les localisations de ces oeuvres. Le script Python fourni permet de remplir la base de données avec des données fictives pour tester le fonctionnement de la base.


## Installation

1. Cloner le repository sur votre machine.

    `https://github.com/VincentPRV/projet_E1.git`

2. Naviguez jusqu'au dossier du projet

3. Installez les dépendances avec la commande suivante :

    `pip install -r requirements.txt`

4. Créez une base de données SQLite avec la commande suivante :

    `python create_db.py`

Ce script va créer une base de données nommée projet_E1.db et y créer les tables nécessaires en exécutant le code SQL du fichier projet.sql.

4. Insérez des données de test dans la base de données en décommentant et en exécutant la fonction `insert_test_data()` dans le fichier create_db.py. Cette fonction va insérer 5 valeurs test dans chaque table de la base de données.

5. Vous pouvez également insérer des données à partir d'un fichier CSV en exécutant la fonction `insert_data_from_dataframe(df)` dans le fichier create_db.py, où df est un DataFrame Pandas contenant les données que vous voulez insérer. Cette fonction va insérer les valeurs du DataFrame dans la base de données.

6. Pour supprimer toutes les données de la base de données, exécutez la fonction `teardown()` dans le fichier create_db.py.

**Note :** les fonctions `insert_test_data()` et `insert_data_from_dataframe(df)` sont destinées à des fins de test uniquement et peuvent être adaptées ou supprimées selon vos besoins.


## Utilisation


### Connexion à la base de données

Pour se connecter à la base de données. Il suffit d'exécuter la commande suivante :

    `sqlite3 projet_E1.db`



### Tables de la base de données

Une fois connecté, vous pouvez voir les tables présentes dans la base de données avec la commande suivante :

`.tables`



### Contenu d'une table

Pour afficher le contenu d'une table, utilisez la commande suivante en remplaçant `nom_table` par le nom de la table souhaitée :

`SELECT * FROM nom_table;`



### Requête pour récupérer toutes les informations liées à un auteur

La requête suivante permet de récupérer toutes les informations liées à un auteur, y compris les informations sur ses oeuvres et leur localisation :

`SELECT auteurs.nom AS auteur, oeuvres.domaine, localisations.ville, localisations.region, localisations.base 
FROM auteurs 
JOIN oeuvres ON auteurs.auteurid = oeuvres.auteurid 
JOIN localisations ON oeuvres.villeid = localisations.villeid 
WHERE auteurs.auteurid = ???;`


## Auteurs

- Vincent Prévot
