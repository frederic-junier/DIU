from functools import wraps

def debug(fonc) :
    print("Debug")
    ''' Un décorateur pour compter le nombre d’appels d’une fonction '''
    @wraps(fonc)
    def wrapped(*args, **kwargs) :
        wrapped.compteur += 1
        print(f'{fonc.__name__} ({args, kwargs})')
        return fonc(*args, *kwargs)
    wrapped.compteur = 0
    print("ouf")
    return wrapped

print("ah")

@debug
def test(x) :
    print("zut")
    return x

print("un")
test(3)

print("deux")
test(3)

# Quand on RUN, on voit qu'il affiche debug une unique fois... un seul unique appel à debug

# Ordre d'éxécution de ces lignes :
# 1       importation...
# 3       création de debug
#15       affichage : 'ah'
#18       crétion de test
#17       décoration de test et appel debug :
# 4           -affichage 'debug'
# 5           -docstring, commentaires...
# 7           -création de wrapped pour remplacer debug
# 6           -décoration de wrapped qui permet de garder le nom de la fonction  
#11           -initialisation compteur
#12           -affichage 'ouf'
#13           -retour wrapped ???
#22        affichage 'un'
#23        appele la fonction test avec paramètre 3, attention on fait d'abord la décoration...
# 8           -incrmentation
# 9           -affichage 'test (((3,), {}))'
#10           -renvoie fct test
#19        affichage 'zut'
#20        renvoie 3 (ss l'afficher)
#25        affichage 'deux'
#26        appele la fonction test avec paramètre 3, attention on fait d'abord la décoration...
# 8           -incrmentation
# 9           -affichage 'test (((3,), {}))'
#10           -renvoie fct test
#19           -affichage 'zut'
#20        renvoie 3 (ss l'afficher)



