import sqlite3

# Créer la base de données
connection = sqlite3.connect("projet_E1.db")

# Créer les tables avec le code SQL fourni
with open("projet.sql") as sql_file:
    query = sql_file.read()
    connection.executescript(query)

# Fermer la connexion à la base de données
connection.close()
