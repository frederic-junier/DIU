.open "LOTBOUTEILLES";

CREATE TABLE "APPELLATION" (
  "idappellation" VARCHAR(42),
  "type" VARCHAR(42),
  "nom" VARCHAR(42),
  PRIMARY KEY ("idappellation")
);

CREATE TABLE "DOMAINE" (
  "iddomaine" VARCHAR(42),
  "nom" VARCHAR(42),
  PRIMARY KEY ("iddomaine")
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

CREATE TABLE "LOTBOUTEILLE" (
  "idlotbouteille" VARCHAR(42),
  "volume" VARCHAR(42),
  "degré" VARCHAR(42),
  "total" VARCHAR(42),
  "prix" VARCHAR(42),
  "commentaire" VARCHAR(42),
  "millésime" VARCHAR(42),
  "idrégion" VARCHAR(42),
  "idappellation" VARCHAR(42),
  "idcuvée" VARCHAR(42),
  "iddomaine" VARCHAR(42),
  "idcouleur" VARCHAR(42),
  PRIMARY KEY ("idlotbouteille"),
  FOREIGN KEY ("idrégion") REFERENCES "RÉGION" ("idrégion"),
  FOREIGN KEY ("idappellation") REFERENCES "APPELLATION" ("idappellation"),
  FOREIGN KEY ("idcuvée") REFERENCES "CUVÉE" ("idcuvée"),
  FOREIGN KEY ("iddomaine") REFERENCES "DOMAINE" ("iddomaine"),
  FOREIGN KEY ("idcouleur") REFERENCES "COULEUR" ("idcouleur")
);

CREATE TABLE "COULEUR" (
  "idcouleur" VARCHAR(42),
  "type" VARCHAR(42),
  PRIMARY KEY ("idcouleur")
);

CREATE TABLE "RÉGION" (
  "idrégion" VARCHAR(42),
  "nom" VARCHAR(42),
  PRIMARY KEY ("idrégion")
);

CREATE TABLE "CUVÉE" (
  "idcuvée" VARCHAR(42),
  "nom" VARCHAR(42),
  PRIMARY KEY ("idcuvée")
);

CREATE TABLE "SITE" (
  "idsite" VARCHAR(42),
  "description" VARCHAR(42),
  PRIMARY KEY ("idsite")
);