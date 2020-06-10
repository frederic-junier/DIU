.open "DOMAINES";

CREATE TABLE "STOCKÉ_À" (
  "idlotbouteille" VARCHAR(42),
  "idsite" VARCHAR(42),
  PRIMARY KEY ("idlotbouteille", "idsite"),
  FOREIGN KEY ("idlotbouteille") REFERENCES "LOTBOUTEILLE" ("idlotbouteille"),
  FOREIGN KEY ("idsite") REFERENCES "SITE" ("idsite")
);

CREATE TABLE "SITE" (
  "idsite" VARCHAR(42),
  "description" VARCHAR(42),
  PRIMARY KEY ("idsite")
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
  PRIMARY KEY ("idlotbouteille"),
  FOREIGN KEY ("iddomaine") REFERENCES "DOMAINE" ("iddomaine")
);

CREATE TABLE "DOMAINE" (
  "iddomaine" VARCHAR(42),
  "nom" VARCHAR(42),
  "idappellation" VARCHAR(42),
  "idrégion" VARCHAR(42),
  PRIMARY KEY ("iddomaine"),
  FOREIGN KEY ("idappellation") REFERENCES "APPELLATION" ("idappellation"),
  FOREIGN KEY ("idrégion") REFERENCES "RÉGION" ("idrégion")
);

CREATE TABLE "DE_LA_CUVÉE" (
  "iddomaine" VARCHAR(42),
  "idcuvée" VARCHAR(42),
  PRIMARY KEY ("iddomaine", "idcuvée"),
  FOREIGN KEY ("iddomaine") REFERENCES "DOMAINE" ("iddomaine"),
  FOREIGN KEY ("idcuvée") REFERENCES "CUVÉE" ("idcuvée")
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