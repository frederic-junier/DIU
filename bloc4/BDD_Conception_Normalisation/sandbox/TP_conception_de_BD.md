Travaux pratiques bases de données : conception
===============================================

**IMPORTANT** : par défaut, la vérification des clefs étrangère n'est pas activée dans SQLite <https://www.sqlite.org/foreignkeys.html>, activez là avec la commande :

```sql
PRAGMA foreign_keys=1;
```


Exercice : variations sur le thème de la clef primaire
-----------------------------------------------

On considère le script SQL suivant :

```sql
CREATE TABLE Classe(
  id INTEGER PRIMARY KEY,
  description TEXT
);

CREATE TABLE Herite(
  enfant INT REFERENCES Classe(id),
  parent INT REFERENCES Classe(id),
  PRIMARY KEY (enfant, parent)
);

INSERT INTO Classe VALUES(0, 'chose');
INSERT INTO Classe VALUES(1, 'animal');
INSERT INTO Classe VALUES(2, 'humain');
INSERT INTO Classe VALUES(3, 'enseignant');
INSERT INTO Classe VALUES(4, 'chat');
INSERT INTO Classe VALUES(5, 'science');

INSERT INTO Herite VALUES(1, 0);
INSERT INTO Herite VALUES(2, 1);
INSERT INTO Herite VALUES(3, 2);
INSERT INTO Herite VALUES(4, 1);
INSERT INTO Herite VALUES(3, 5);
```

**Exercice** : on veut s'habituer aux messages d'erreurs standards :

* insérez un nouveau tuple avec `INSERT INTO Classe VALUES(0, 'patate');`. Quel est le message d'erreur ? Idem avec `INSERT INTO Herite VALUES(1, 0);`
* insérez un nouveau tuple avec `INSERT INTO Herite VALUES(0, 42);`. Quel est le message d'erreur ? (_NB_ : si vous n'en avez pas, c'est que les clefs étrangères ne sont pas activées !)

**Exercice** : dessinez un diagramme Entité-Association du schéma de cette base. Ensuite, dessinez le graphe de la relation `Herite` : il s'agit de représenter graphiquement _le contenu_ de  `Herite` par une hiérarchie entre les classes, typiquement avec les parents en haut, les fils en dessous avec des arcs orientés des fils vers les parents pour les relier.

**Exercice** : si on remplace `PRIMARY KEY (enfant, parent)` par la contrainte `PRIMARY KEY (enfant)` dans la définition de `Herite` : 

  * quelle restriction est imposée sur les hiérarchies de classes que cette base peut représenter ? 
  * quel est le changement correspondant dans le diagramme E/A ? 
  * si on retraduit le diagramme E/A en schéma SQL, quel schéma obtiendra-t'on ?

**Exercice** : mêmes questions que précédemment si on remplace `PRIMARY KEY (enfant, parent)` par la contrainte `PRIMARY KEY (parent)` .

**Exercice** : mêmes questions que précédemment si on enlève simplement la contrainte `PRIMARY KEY (enfant, parent)`.

Exercice : reprise de la base _Stanford_
---------------------------------------

On reprend la base _Stanford_ d'exemple de la première partie.
Le script de création de table est le suivant.

```sql
create table College(
    cName varchar(255),
    state varchar(255),
    enrollment int);
    
create table Student(
    sID int,
    sName varchar(255),
    GPA real, -- Grade Point Average, out of 4
    sizeHS int);

create table Apply(
  sID int,
  cName varchar(255),
  major varchar(255),
  decision char(1));
```

**Exercice** : Reprenez le fichier `base-stanford.sql` du TP1 et modifiez le schéma pour y ajouter les contraintes d'intégrité (clef primaire et clef étrangères) attendues. Après modification, _toutes_ les données d'exemple de la base doivent pouvoir être insérées sans erreurs.

**Exercice** : SQL propose un type de contrainte assez générique appelée `CHECK`, définissez en pour les attributs [_GPA_](https://en.wikipedia.org/wiki/Academic_grading_in_the_United_States#Numerical_and_letter_grades) et _decision_. Là encore, toutes les données doivent pouvoir s'importer correctement après ajout des contraintes supplémentaires.

On remarque que dans cette base, les disciplines sont identifiées par une chaîne de caractères non normalisée (casse variable, abréviations). On va donc créer une table pour les disciplines et utiliser les requêtes d'insertion et de mise-à-jour. Quelques liens de documentation :

 * `INSERT` <https://www.sqlite.org/lang_insert.html> et <https://www.sqlitetutorial.net/sqlite-insert/>
 * `UPDATE` <https://www.sqlitetutorial.net/sqlite-update/> et <https://www.sqlite.org/lang_update.html>


**Exercice** : avec une requête, déterminez la valeur de _major_ la plus longue. Il faudra un agrégat et trouver la bonne fonction sur les chaînes dans la documentation <https://www.sqlite.org/lang_corefunc.html>.

**Exercice** : définir une nouvelle table `Major` avec comme attributs _code_ qui est clef et un autre attribut _description_. Peuplez ensuite cette table en utilisant l'attribut _major_ de `Apply`  (avec une requête `INSERT INTO Apply SELECT ...`). Lors de l'import, normalisez l'attribut _code_ pour que toutes ses valeurs soient en majuscule. Pour la description, vous pouvez remplir avec le code dans un premier temps puis éditer à la main (e.g., pour _EE_ on voudrait lire _Electrical Engineering_). 

**Exercice** : on souhaite mettre à jour la table `Apply` et ajouter la contrainte de clef étrangère vers la table `Major` nouvellement créée. Malheureusement, SQLite ne permet pas les opérations (<https://www.sqlite.org/omitted.html>) nécessaires. Ainsi à la place

 . créez une table `Apply2` avec toutes les contraintes,
 . insérez le contenu de `Apply` dans `Apply2`,
 . supprimez `Apply` (commande `DROP TABLE ...`),
 . enfin renommez `Apply2` en  `Apply` (commande `ALTER TABLE ....`).




Exercice : modélisation
-----------------------

Cet exercice est proposé dans le fichier pdf [`cas_d_etude_modelisation.pdf`](cas_d_etude_modelisation.pdf).

