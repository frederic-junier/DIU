-- POUR CHARGER DANS SQLite3 : 
-- sqlite3 join_algorithms_versus_sqlite3.db
-- .timer on
-- .read join_algorithms_schema.sql

drop table if exists Table1;
drop table if exists Table2;

-- Un schéma très simple, qui reprend le benchmark des 3 algos en Python qu'on rappelle ici :
--
-- def benchmark(size_1=1000, nb_val_1=100,
--               size_2=1000, nb_val_2=100,
--               nb_repeat=100,
--               bench_loop=True, bench_hash=True, bench_merge=True):
--
--    sample_1 = [(i, randrange(nb_val_1)) for i in range(size_1)]
--    sample_2 = [(randrange(nb_val_2), 'A'+str(j)) for j in range(size_2)]

-- Activation des clefs étrangères
PRAGMA foreign_keys=1; 

create table Table1(
    idA INTEGER PRIMARY KEY,    -- un ID entier
    val INTEGER     -- l'attribut de jointure
);

create table Table2(
    val INTEGER,  -- pas  REFERENCES Table1(val), mais ca ne changerait rien
    idB INTEGER
);


 -- On va remplir les tables avec 10.000 lignes pour A et autant pour B
  
WITH RECURSIVE data_1(val) AS (
  SELECT 1
  UNION ALL
  SELECT val+1
  FROM data_1
  WHERE val+1 <= 10000
) 
INSERT INTO Table1 
  SELECT  val,
          ABS(RANDOM() % 1000)
  FROM data_1;

WITH RECURSIVE data_2(val) AS (
  SELECT 1
  UNION ALL
  SELECT val+1
  FROM data_2
  WHERE val+1 <= 10000
) 
INSERT INTO Table2
  SELECT  ABS(RANDOM() % 1000),
          'A' || val
  FROM data_2;
