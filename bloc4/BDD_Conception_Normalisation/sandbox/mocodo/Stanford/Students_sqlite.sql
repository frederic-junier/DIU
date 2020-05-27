.open "APPLYS";

CREATE TABLE "APPLY" (
  "id" VARCHAR(42),
  "sid" VARCHAR(42),
  "cname" VARCHAR(42),
  "major" VARCHAR(42),
  "decision" VARCHAR(42),
  "cname_1" VARCHAR(42),
  "sid_1" VARCHAR(42),
  PRIMARY KEY ("id"),
  FOREIGN KEY ("cname_1") REFERENCES "COLLEGE" ("cname"),
  FOREIGN KEY ("sid_1") REFERENCES "STUDENT" ("sid")
);

CREATE TABLE "STUDENT" (
  "sid" VARCHAR(42),
  "sname" VARCHAR(42),
  "gpa" VARCHAR(42),
  "sizehs" VARCHAR(42),
  PRIMARY KEY ("sid")
);

CREATE TABLE "COLLEGE" (
  "cname" VARCHAR(42),
  "state" VARCHAR(42),
  "enrollment" VARCHAR(42),
  PRIMARY KEY ("cname")
);