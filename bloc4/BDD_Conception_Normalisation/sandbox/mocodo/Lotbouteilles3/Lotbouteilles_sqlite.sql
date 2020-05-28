.open "LOTBOUTEILLES";

CREATE TABLE "DÉGUSTATION" (
  "iddégustation" VARCHAR(42),
  "date" VARCHAR(42),
  "idlotbouteille" VARCHAR(42),
  "idlotbouteille_1" VARCHAR(42),
  PRIMARY KEY ("iddégustation"),
  FOREIGN KEY ("idlotbouteille_1") REFERENCES "LOTBOUTEILLE" ("idlotbouteille")
);

CREATE TABLE "RÉGION" (
  "idrégion" VARCHAR(42),
  "nom" VARCHAR(42),
  PRIMARY KEY ("idrégion")
);

CREATE TABLE "APPELLATION" (
  "idappellation" VARCHAR(42),
  "type" VARCHAR(42),
  "nom" VARCHAR(42),
  PRIMARY KEY ("idappellation")
);

CREATE TABLE "LOTBOUTEILLE" (
  "idlotbouteille" VARCHAR(42),
  "volume" VARCHAR(42),
  "degré" VARCHAR(42),
  "prix" VARCHAR(42),
  "couleur" VARCHAR(42),
  "commentaire" VARCHAR(42),
  "millésime" VARCHAR(42),
  "iddomaine" VARCHAR(42),
  "iddomaine_1" VARCHAR(42),
  PRIMARY KEY ("idlotbouteille"),
  FOREIGN KEY ("iddomaine_1") REFERENCES "DOMAINE" ("iddomaine")
);

CREATE TABLE "DOMAINE" (
  "iddomaine" VARCHAR(42),
  "nom" VARCHAR(42),
  "idrégion" VARCHAR(42),
  "idcuvée" VARCHAR(42),
  "idappellation" VARCHAR(42),
  "idappellation_1" VARCHAR(42),
  "idcuvée_1" VARCHAR(42),
  "idrégion_1" VARCHAR(42),
  PRIMARY KEY ("iddomaine"),
  FOREIGN KEY ("idappellation_1") REFERENCES "APPELLATION" ("idappellation"),
  FOREIGN KEY ("idcuvée_1") REFERENCES "CUVÉE" ("idcuvée"),
  FOREIGN KEY ("idrégion_1") REFERENCES "RÉGION" ("idrégion")
);

CREATE TABLE "STOCKAGE" (
  "idlotbouteille" VARCHAR(42),
  "idsite" VARCHAR(42),
  "nombre" VARCHAR(42),
  "idlotbouteille_1" VARCHAR(42),
  "idsite_1" VARCHAR(42),
  PRIMARY KEY ("idlotbouteille", "idsite"),
  FOREIGN KEY ("idlotbouteille_1") REFERENCES "LOTBOUTEILLE" ("idlotbouteille"),
  FOREIGN KEY ("idsite_1") REFERENCES "SITE" ("idsite")
);

CREATE TABLE "SITE" (
  "idsite" VARCHAR(42),
  "description" VARCHAR(42),
  PRIMARY KEY ("idsite")
);

CREATE TABLE "CUVÉE" (
  "idcuvée" VARCHAR(42),
  "nom" VARCHAR(42),
  PRIMARY KEY ("idcuvée")
);