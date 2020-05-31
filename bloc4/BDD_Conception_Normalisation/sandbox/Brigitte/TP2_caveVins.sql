PRAGMA foreign_keys=1;

DROP TABLE if EXISTS Site;
DROP TABLE if EXISTS Stockage;
DROP TABLE if EXISTS Dégustation;
DROP TABLE if EXISTS LotBouteille;
DROP TABLE if EXISTS Région;
DROP TABLE if EXISTS Domaine;
DROP TABLE if EXISTS Cuvée; 
DROP TABLE if EXISTS Commentaires;

CREATE TABLE Site(
    idSite INTEGER NOT NULL PRIMARY KEY,
	lieuStockage TXT,
	précision Stockage VARCHAR(1) CHECK (précision IN ('H','B'))
	);

CREATE TABLE Stockage (
    idStockage INTEGER NOT NULL PRIMARY KEY,
    idLotBouteille INTEGER NOT NULL REFERENCES LotBouteille (idLotBouteille),
    idSite INTEGER NOT NULL REFERENCES SITE (idSite),
    nombre INTEGER NOT NULL   -- faire une somme sur différents sites contenant même bouteilles...
    );

CREATE TABLE LotBouteille(
    idLotBouteille INTEGER NOT NULL PRIMARY KEY,
    idCommentaires INTEGER NOT NULL REFERENCES Commentaires(idCommentaires),
	idDomaine INTEGER NOT NULL REFERENCES Domaine(idDomaine),
    couleur VARCHAR(5) CHECK(LOWER(couleur) IN ('rouge','rose','blanc')),
	volume REAL NOT NULL CHECK(volume >= 0),
    millésime INTEGER CHECK(millésime >= 0),
	degré REAL CHECK(degré >= 0)  -- Attention il faudra nettoyer % °
    );

CREATE TABLE Dégustation (
    idDégustation INTEGER NOT NULL PRIMARY KEY,
    idStockage INTEGER NOT NULL REFERENCES Stockage(idStockage),
	dateDégustation TXT,
    commentairesDégustation TXT 
    );

CREATE TABLE Région (
    idRégion INTEGER NOT NULL PRIMARY KEY,
    nomRégion TXT NOT NULL UNIQUE,
	appellation TXT
    );

CREATE TABLE Domaine (
    idDomaine INTEGER NOT NULL PRIMARY KEY,
	idRegion INTEGER NOT NULL REFERENCES Région(idRégion),
    idCuvée INTEGER NOT NULL REFERENCES Cuvée(idCuvée),
	nomDomaine TXT    -- un nom de domaine n'est pas forcément unique 
    );

CREATE TABLE Cuvée (
    idCuvée INTEGER NOT NULL PRIMARY KEY,
    nomCuvée TXT UNIQUE   --un nom de cuvée est unique mais peut être vide
    );

CREATE TABLE Commentaires (
    idCommentaires INTEGER NOT NULL PRIMARY KEY,
    prix REAL CHECK(prix >= 0),
    descriptionDégustation TXT
	);
	

