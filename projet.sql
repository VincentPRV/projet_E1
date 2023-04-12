CREATE TABLE IF NOT EXISTS localisations(
    villeid INTEGER PRIMARY KEY AUTOINCREMENT,
    base        VARCHAR(255) NOT NULL,
    pop_coordonnees     INTEGER,
    region      VARCHAR(255),
    ville       VARCHAR(255) UNIQUE
);

CREATE TABLE IF NOT EXISTS auteurs(
    auteurid   INTEGER PRIMARY KEY AUTOINCREMENT,
    nom   VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS oeuvres(
    oeuvreid    INTEGER PRIMARY KEY,
    villeid    INTEGER,
    domaine     VARCHAR(255),
    auteurid INTEGER NOT NULL, 
    FOREIGN KEY(auteurid) REFERENCES auteurs(auteurid),
    FOREIGN KEY (villeid) REFERENCES localisations(villeid)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);
