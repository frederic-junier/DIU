# Activité _Notice de montage_



## Sujet choisi

Illustration du tri topologique dans un contexte et implémentation de ce tri comme méthode d'une classe d'objets graphes orientés.

L'ensemble de fichiers de cette activité sont disponibles en ligne sur ce dépôt <https://github.com/frederic-junier/DIU-Junier/tree/master/bloc5/Graphes/sandbox/Graphes_Lib_Stud/DM>.

## Contenu de l'archive et mode d'emploi

* Une fois déballée, cette archive contient cinq fichiers :

.

├── activite-eleve.md

├── LibGraphesJunierFrederic.py

├── MainJunierFrederic.py

├── Makefile

└── README.md

* `README.md` est ce fichier
* `LibGraphesJunierFrederic.py` est le fichier contenant la bibliothèque de graphes avec deux classes `Graph` et `DirectGraph` qui hérite de `Graph`. La documentation de la classe `DirectGraph` contient une série de tests d'exécution des différentes méthodes de classes sur quelques exemples. Ils peuvent être vérifiés automatiquement avec le module `doctest` lorsqu'on exécute le fichier directement `LibGraphesJunierFrederic.py`. 
* `MainJunierFrederic.py` est le fichier de tests avec un jeu de tests réduit, à compléter par els élèves,  il peut s'exécuter avec des options :
  * `python3 MainJunierFrederic.py` exécute le script sans générer de fichiers `pdf` et `png` pour les graphes manipulés, les sorties des tests sont affichées dans la console
  * `python3 MainJunierFrederic.py h` ou `python3 MainJunierFrederic.py -h` affiche l'aide (réduite) du programme
  * `python3 MainJunierFrederic.py pdf` ou `python3 MainJunierFrederic.py png` exécute les tests, affiche les sorties dans la console, 
  crée un sous-répertoire `images` dans le répertoire de l'archive et y stocke les fichiers `pdf` et `png` des graphes générés avec les outils de la ligne de commande `xargs` et `convert`.

* `activite-eleve.md` contient une ébauche de scénario d'activité élève en langage Markdown. Le contenu est le même que dans la partie Contexte ci-dessous avec en plus les dessins des graphes.  Pour générer les versions `pdf` et `odt` de l'activité, il suffit d'ouvrir un terminal de commande dans le répertoire courant et  d'exécuter la commande `make` ou `make all`. Le script `MainJunierFrederic.py` est alors exécuté avec l'option `pdf`, les fichiers `pdf` et `png` des graphes  sont générés dans le sous-répertoire `images` et les fichiers `activite-eleve.pdf` et `activite-eleve.odt` sont générés avec `pandoc` à partir de la source `activite-eleve.md`. On peut nettoyer   les fichiers créés en exécutant `make clean` et si on a modifié le contenu d'un fichier source on peut tout reconstruire avec `make fres`. Pour outiller l'activité, il faudra fournir aux élèves un code à trous avec des `# TO DO` à compléter au niveau des différentes méthodes à compléter.


## Contexte de l'activité


Vous travaillez au service _Notice de montage_ de l'entreprise  __AEKI__ qi fabrique et commercialise des meubles en kit, _à monter soi-même_.

Pour chaque nouveau produit, le service ingénierie vous founit un schéma sous la forme d'un _graphe de contraintes_ qui est un graphe orienté :
*  chaque étape de montage  est un sommet du graphe, identifié par une étiquette distincte choisie aléatoirement  parmi les  lettres minuscules 
*  un arc reliant deux sommets du graphe exprime une contrainte d'ordre (ou _relation de précédence_ ou _relation de dépendance_) dans le montage  : par exemple un arc d'origine  le sommet d'étiquette `'c'` et d'extrémité le sommet d'étiquette  `'a'`  signifie que  l'étape de montage `'c'` doit être réalisée avant l'étape `'a'`.
  
Attention, L'étiquetage étant aléatoire, l'ordre alphabétique sur les étiquettes des étapes n'est pas forcément l'ordre de montage !
À partir d'un tel graphe, vous devez définir un ordre d'exécution des étapes de montage pour la notice de montage, permettant à un utilisateur de monter le produit en respectant toutes les contraintes.

Le fichier `activite-eleve.md` contient un scénario plus détaillé de l'activité élève, voici uen synthèse des questions possibles

1. Le service ingénierie vous a fourni un graphe de contraintes ci-dessous, vous devez vérifier si l'ordre de montage (voir activité élève)  respecte  les contraintes du graphe. Si ce n'est pas le cas, vous devez proposer une modification de  cet ordre qui  respecte les contraintes du graphe. On peut aussi se demander s'il existe d'autres ordres possibles pour la notice de montage.

2. Le service ingénierie vous a fourni un autre graphe (qui contient un cycle, voir activité élève). 

    * Pouvez-vous déterminer un ordre de montage respectant ces contraintes ?
    * Quelle condition nécessaire doit vérifier un graphe de contraintes pour qu'un ordre de montage existe ? On admet que cette condition nécessaire est suffisante, c'est-à-dire que si elle est vérifiée alors un ordre de montage existe.

3. Votre chef vous demande d'écrire en pseudo-code  un algorithme qui automatise la génération d'un ordre de montage à partir d'un ugraphe de contraintes pour lequel il existe un ordre de montage.
Ayant suivi la spécialité NSI au lycée, vous vous souvenez des algorithmes gloutons présentés en classe de première.

   * Citez au moins un algorithme glouton que vous avez déjà rencontré.
   * Dans le cadre de votre problème, pour obtenir un ordre de montage compatible avec le graphe, quel choix  glouton peut-on faire à chaque étape ?
   * Complétez l'écriture en pseudo-code d'un algorithme glouton qui permettrait de déterminer un ordre de montage compatible avec un graphe donné.
   * Déroulez cet algorithme sur le graphe de contraintes donné en question 1.
   * On ne demande pas de démontrer que l'algorithme est correct, mais pouvez-vous estimer la complexité de votre algorithme en fonction du nombre d'étapes de montage (sommets du graphe) et du nombre d'arêtes (les contraintes) ?
   * Un ordre de montage pour un graphe de contraintes s'appelle un __ordre topologique__ sur les sommets du graphe. Implémentez votre algorithme en `Python` en complétant la méthode `topological_sort_greedy` de la classe `DirectGraph` dans le  fichier `LibGraphes.py`. Commencez par lire la documentation de la classe `DirectGraph`.
   * Testez votre méthode avec le fichier `Main.py`.
   * Complétez le code de la  méthode `verif_topological_order`  de la classe `DirectGraph` dans le  fichier `LibGraphes.py` pour qu'elle vérifie si un ordre de montage donné en paramètre est bien compatible avec le graphe de contraintes.


4. Il existe un autre algorithme pour déterminer un ordre topologique sur les sommets d'un graphe, basé sur un parcours en profondeur du graphe. 
   
   * Visionnez ce tutoriel video <https://youtu.be/eVsCO71q1L0>, puis implémentez cet algorithme en complétant la méthode `topological_sort_dfs` de la classe `DirectGraph` dans le  fichier `LibGraphes.py`.
   * Testez votre méthode avec le fichier `Main.py`. 



-----------------------------


# Références :

* Sitographie :
  * Article _S’aider des graphes pour élaborer une notice de montage_   dont l'URL est   <https://interstices.info/saider-des-graphes-pour-elaborer-une-notice-de-montage/>
