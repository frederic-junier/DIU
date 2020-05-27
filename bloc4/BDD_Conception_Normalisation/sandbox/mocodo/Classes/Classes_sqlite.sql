.open "CLASSE_ENFANTS";

CREATE TABLE "CLASSE" (
  "id" VARCHAR(42),
  "description" VARCHAR(42),
  PRIMARY KEY ("id")
);

CREATE TABLE "HERITE" (
  "id" VARCHAR(42),
  "id_1" VARCHAR(42),
  PRIMARY KEY ("id", "id_1"),
  FOREIGN KEY ("id") REFERENCES "CLASSE" ("id"),
  FOREIGN KEY ("id_1") REFERENCES "CLASSE" ("id")
);