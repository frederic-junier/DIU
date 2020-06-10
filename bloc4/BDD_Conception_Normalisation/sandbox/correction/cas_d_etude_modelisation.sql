------------------------------------------------------------
--        Script SQLite  
------------------------------------------------------------


------------------------------------------------------------
-- Table: domaine
------------------------------------------------------------
CREATE TABLE domaine(
	nom        TEXT NOT NULL PRIMARY KEY,
	adresse    TEXT NOT NULL
);


------------------------------------------------------------
-- Table: region
------------------------------------------------------------
CREATE TABLE region(
	nom    TEXT NOT NULL PRIMARY KEY
);


------------------------------------------------------------
-- Table: appellation
------------------------------------------------------------
CREATE TABLE appellation(
	nom           TEXT NOT NULL PRIMARY KEY,
	type          TEXT NOT NULL ,
	nom_region    TEXT NOT NULL REFERENCES region(nom)
);


------------------------------------------------------------
-- Table: cuvee
------------------------------------------------------------
CREATE TABLE cuvee(
	nom_domaine        TEXT NOT NULL REFERENCES domaine(nom),
	nom_appellation    TEXT NOT NULL REFERENCES appellation(nom),
	nom                TEXT NOT NULL ,
	annee              NUMERIC NOT NULL ,
	couleur            TEXT NOT NULL CHECK( couleur IN ('rouge', 'blanc', 'rosé')),
	degres             REAL NOT NULL CHECK( degres BETWEEN 8.0 AND 18.0),
	PRIMARY KEY (nom_domaine,nom_appellation,nom,annee)
);


------------------------------------------------------------
-- Table: stockage
------------------------------------------------------------
CREATE TABLE stockage(
	lieu      TEXT NOT NULL PRIMARY KEY,
	detail    TEXT NOT NULL
);



------------------------------------------------------------
-- Table: stocker
------------------------------------------------------------
CREATE TABLE stocker(
	lieu      TEXT NOT NULL REFERENCES stockage(lieu),
	nom_domaine        TEXT NOT NULL REFERENCES domaine(nom),
	nom_appellation    TEXT NOT NULL REFERENCES appellation(nom),
	nom       TEXT NOT NULL ,
	annee     INTEGER NOT NULL CHECK( annee BETWEEN 1700 AND 2100),
	nombre    INTEGER NOT NULL CHECK( nombre > 0),
	PRIMARY KEY (lieu,nom_domaine,nom_appellation,nom,annee),
	FOREIGN KEY (nom,annee) REFERENCES cuvee(nom,annee)
);


------------------------------------------------------------
-- Table: acheter
------------------------------------------------------------
CREATE TABLE acheter(
	date      TEXT NOT NULL ,
	nom_domaine        TEXT NOT NULL REFERENCES domaine(nom),
	nom_appellation    TEXT NOT NULL REFERENCES appellation(nom),
	nom       TEXT NOT NULL ,
	annee     NUMERIC NOT NULL ,
	prix      NUMERIC ,
	nombre    INTEGER NOT NULL CHECK( nombre > 0),
	PRIMARY KEY (date,nom_domaine,nom_appellation,nom,annee),
	FOREIGN KEY (nom,annee) REFERENCES cuvee(nom,annee)
);



