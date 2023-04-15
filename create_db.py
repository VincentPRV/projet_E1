import sqlite3
import pandas as pd


def exe_sql():
    """
    Execution du SQL de la page projet.sql, servant principalement à la création des tables et leurs paramètres.
    """
    # Créer la base de données
    connection = sqlite3.connect("projet_E1.db")

    # Créer les tables avec le code SQL fourni
    with open("projet.sql") as sql_file:
        query = sql_file.read()
        connection.executescript(query)

    # Fermer la connexion à la base de données
    connection.close()

def insert_test_data():
    # Se connecter à la base de données
    connection = sqlite3.connect("projet_E1.db")
    
    # Insérer 5 valeurs test dans chaque table
    for i in range(1, 6):
        # Insérer une valeur test dans la table localisations
        base = f"base{i}"
        pop_coordonnees = i * 100
        region = f"region{i}"
        ville = f"ville{i}"
        connection.execute("INSERT OR IGNORE INTO localisations(base, pop_coordonnees, region, ville) VALUES (?, ?, ?, ?)", (base, pop_coordonnees, region, ville))
        villeid = connection.execute("SELECT last_insert_rowid()").fetchone()[0]
        
        # Insérer une valeur test dans la table auteurs
        nom = f"auteur{i}"
        connection.execute("INSERT OR IGNORE INTO auteurs(nom) VALUES (?)", (nom,))
        auteurid = connection.execute("SELECT last_insert_rowid()").fetchone()[0]
        
        # Insérer une valeur test dans la table oeuvres
        domaine = f"domaine{i}"
        connection.execute("INSERT OR IGNORE INTO oeuvres(domaine, auteurid, villeid) VALUES (?, ?, ?)", (domaine, auteurid, villeid))
    
    # Valider les modifications
    connection.commit()
    
    # Fermer la connexion à la base de données
    connection.close()



def insert_data_from_dataframe(df, max_rows=None):
    # Se connecter à la base de données
    connection = sqlite3.connect("projet_E1.db")
    
    # Insérer les valeurs du dataframe dans chaque table
    for i, row in df.iterrows():
        if max_rows is not None and i >= max_rows:
            break
        
        # Insérer une valeur dans la table localisations
        base = row["BASE"]
        pop_coordonnees = row["POP_COORDONNEES"]
        region = row["REGION"]
        ville = row["Ville_"]
        result = connection.execute("SELECT villeid FROM localisations WHERE ville = ?", (ville,)).fetchone()
        if result is None:
            cursor_used = connection.execute("INSERT INTO localisations(base, pop_coordonnees, region, ville) VALUES (?, ?, ?, ?)", (base, pop_coordonnees, region, ville))
            villeid = cursor_used.lastrowid
        else:
            villeid = result[0]

        # Insérer une valeur ou plusieurs valeurs dans la table auteurs
        auteurs = row["Auteur"]
        
        if isinstance(auteurs, str):
            auteurs = [auteurs]  # Transformer la chaîne de caractères en liste

        for nom in auteurs:
            result = connection.execute("SELECT auteurid FROM auteurs WHERE nom = ?", (nom,)).fetchone()
            if result is None:
                cursor_used = connection.execute("INSERT INTO auteurs(nom) VALUES (?)", (nom,))
                auteurid =  cursor_used.lastrowid
            else:
                auteurid = result[0]
        
            # Insérer une valeur dans la table oeuvres
            domaine = row["Domaine"]
            connection.execute("INSERT INTO oeuvres(domaine, auteurid, villeid) VALUES (?, ?, ?)", (domaine, auteurid, villeid))
    
    # Valider les modifications
    connection.commit()

       
def teardown():
    connection = sqlite3.connect("projet_E1.db")
    cursor = connection.cursor()

    cursor.execute("DELETE FROM localisations")
    cursor.execute("DELETE FROM auteurs")
    cursor.execute("DELETE FROM oeuvres")

    connection.commit()
    connection.close()


if __name__ == "__main__":
        
    exe_sql()
 
    run_tests = False   # Définir la variable pour exécuter ou non les tests

    if run_tests:
        teardown()
        insert_test_data()
        
        # Test 1: Vérifier que la base de données a bien été créée
        connection = sqlite3.connect("projet_E1.db")
        resultat = connection.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        tables = sorted([row[0] for row in resultat.fetchall()])
        attendu = ["auteurs", "localisations", "oeuvres"]
        assert tables == attendu, f"Erreur: Résultat attendu: {attendu}, Résultat obtenu: {tables}"
        print("=" * 10, "Vérification de la création de la base de données réussi", "=" * 10)
        print('')


        # Test 2: Vérifier que les 5 valeurs test ont été insérées dans chaque table
        connection = sqlite3.connect("projet_E1.db")
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM localisations")
        result = cursor.fetchone()[0]
        expected_result = 5
        assert result == expected_result, f"Erreur: Résultat attendu: {expected_result}, Résultat obtenu: {result}"

        cursor.execute("SELECT COUNT(*) FROM auteurs")
        result = cursor.fetchone()[0]
        expected_result = 5
        assert result == expected_result, f"Erreur: Résultat attendu: {expected_result}, Résultat obtenu: {result}"
        
        cursor.execute("SELECT COUNT(*) FROM oeuvres")
        result = cursor.fetchone()[0]
        expected_result = 5
        assert result == expected_result, f"Erreur: Résultat attendu: {expected_result}, Résultat obtenu: {result}"
        print("=" * 10, "Vérification de l'insertion des valeurs test réussi", "=" * 10)
        print('')
        teardown()
        
        
        # Test 3: Vérifier que les données ont été insérées depuis le dataframe
        df = pd.DataFrame({
            "Auteur": ["auteur1", ["auteur2", "auteur5"], "auteur3"],
            "Domaine": ["domaine1", "domaine2", "domaine3"],
            "Ville_": ["ville1", "ville2", "ville3"],
            "BASE": ["base1", "base2", "base3"],
            "POP_COORDONNEES": [100, 200, 300],
            "REGION": ["region1", "region2", "region3"]
        })
        
        insert_data_from_dataframe(df)

        connection = sqlite3.connect("projet_E1.db")
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM localisations")
        result = cursor.fetchone()[0]
        expected_result = 3
        assert result == expected_result, f"Erreur: Résultat attendu: {expected_result}, Résultat obtenu: {result}"
        
        cursor.execute("SELECT COUNT(*) FROM auteurs")
        result = cursor.fetchone()[0]
        expected_result = 4
        assert result == expected_result, f"Erreur: Résultat attendu: {expected_result}, Résultat obtenu: {result}"
        
        cursor.execute("SELECT COUNT(*) FROM oeuvres")
        result = cursor.fetchone()[0]
        expected_result = 4
        assert result == expected_result, f"Erreur: Résultat attendu: {expected_result}, Résultat obtenu: {result}"
        print("=" * 10, "Vérification de l'insertion des données depuis le dataframe test réussi", "=" * 10)
        print('')
        
        # teardown()
                
       