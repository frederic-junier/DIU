####################
#    Classe Pile   #
####################
# Construire une classe implémentant les piles (sans utiliser le module queue de Python), incluant :
# • un constructeur de paramètres self et une liste L
# • un attribut liste (du type list classique de Python)
# • la surcharge de la méthode d’affichage
# • des méthodes empiler, depiler, sommet, estVide, hauteur et traiter

class Pile:
    def __init__(self,L=list()):
        self.pile = L
        
    def __len__(self):
        #correspond à la fonction hauteur ou faut il renommer...
        return len(self.pile)
    
    def __str__(self):
        #surcharge de la méthode d’affichage
        pi = "Etat de la pile:\n"
        for k in self.pile :
            pi +=  str(k) + " "   
        return pi
    
    def empiler(self, valeur):
        '''Procédure où valeur est ajouté en sommet de la pile'''
        #le sommet est à droite...
        self.pile.append(valeur)
        
    def depiler(self):
        '''Procédure qui dépile le sommet de la pile.
        Précondition : la pile n’est pas vide'''
        if len(self.pile) == 0:
             print("On ne dépile pas une pile vide !")
        else :
            self.pile.pop()
        
    def traiter(self):
        '''Fonction qui dépile le sommet de la pile et renvoie ce sommet.
        Précondition : la pile n’est pas vide'''
        if len(self.pile) == 0:
             return "La pile est vide !"
        return self.pile.pop()
    
    def sommet(self):
        '''Fonction qui retourne le sommet de la pile
        Précondition : la pile n’est pas vide'''
        if len(self.pile) == 0:
             return "On ne dépile pas une pile vide !"
        return self.pile[-1]
    
    def estVide(self):
        '''Fonction qui retourne vrai si la pile est vide, faux sinon'''
        return len(self) == 0
    
# p = Pile([])
# print(p.estVide())
# p.depiler()
# p.empiler(3)
# p.empiler(5)
# p.empiler(8)
# print(p)
# print(p.estVide())
# p.depiler()
# print(p.traiter())
# print(p.sommet())
# print(p.traiter())
# print(p.sommet())
# print(p.estVide())
# 
# ####################
# #    Classe File   #
# ####################
# # Construire une classe implémentant les files (sans utiliser le module queue de Python), incluant :
# # • un constructeur de paramètres self et une liste L
# # • un attribut liste (du type list classique de Python)
# # • la surcharge de la méthode d’affichage
# # • des méthodes traiter, enfiler, estVide et longueur
# 
# class File:
#     def __init__(self,L=list()):
#         self.file = L
#         
#     def __len__(self):
#         #correspond à la fonction longueur ou faut il renommer...
#         return len(self.file)
#     
#     def __str__(self):
#         #surcharge de la méthode d’affichage
#         fi = "Etat de la file:\n"
#         for k in self.file :
#             fi +=  str(k) + " "   
#         return fi
#     
#     def enfiler(self, valeur):
#         '''Procédure où valeur est ajouté en sommet de la file'''
#         #on ajoute à droite = queue de la file...
#         self.file.append(valeur)
#         
#     def traiter(self):
#         '''Fonction qui dépile le sommet de la file et renvoie ce sommet.
#         Précondition : la file n’est pas vide'''
#         if len(self) == 0:
#              return "La file est vide !"
#         return self.file.pop(0)  
#    
#     def estVide(self):
#         '''Fonction qui retourne vrai si la file est vide, faux sinon'''
#         return len(self) == 0
#     
# print()
# print()
# f = File([])
# print(f.estVide())
# f.enfiler(3)
# f.enfiler(5)
# f.enfiler(8)
# f.enfiler(18)
# f.enfiler(28)
# f.enfiler(38)
# f.enfiler(48)
# print(f)
# print(f.estVide())
# print(f.traiter())
# print(f.traiter())
# print(f)
# print(f.estVide())
# 
# 
# ################################################
# #  Inversion d'une File en utilisant une Pile  #
# ################################################
# # Le but de cet exercice est d’écrire en Python une procédure qui inverse une file d'éléments
# # qui lui est passée en paramètre. On demande de ne pas utiliser de tableau ou de liste de
# # travail pour effectuer l'inversion, mais d'utiliser plutôt une pile. 
# # Il existe en effet une méthode très simple pour inverser une file en utilisant une pile.
# 
# def inverseFile(file) :
#     p = Pile()
#     for i in range(len(file)) :
#         p.empiler(file.traiter())
#     for i in range(len(p)) :
#         file.enfiler(p.traiter())
#     return file#attention à faire en procedure... var glob ? interet ???
#     
# invf = inverseFile(f)
# print(invf)
# print()
# print()

################################################
#  Validité du parenthésage d'une expression   #
################################################
# Un problème fréquent pour les compilateurs et les traitements de textes est de déterminer si les 
# parenthèses d’une chaîne de caractères sont équilibrées et proprement incluses les unes dans les autres.
# On désire donc écrire une fonction qui teste la validité du parenthésage d’une expression :
# – on considère que les expressions suivantes sont valides : "()", "[([bonjour+]essai)7plus- ];"
# – alors que les suivantes ne le sont pas : "(", ")(", "4(essai]".
# Le but est d’évaluer la validité d’une expression en ne considérant que ses parenthèses et ses crochets. 
# On suppose que l’expression à tester est dans une chaîne de caractères, dont on peut ignorer tous les 
# caractères autres que ‘(’, ‘[’, ’]’ et ‘)’.
# Écrire en Python la fonction valide qui renvoie vrai si l’expression passée en paramètre est valide,
# faux sinon.

def valide(expression) :
    parenth = Pile([])
    for car in expression :
        print(parenth.sommet())
        if car in '([' :
            parenth.empiler(car)
            #print(parenth)
        elif car == ')' and parenth.sommet() == '(':
            parenth.depiler()
            #print(parenth)
        elif car == ']' and parenth.sommet() == '[':
            parenth.depiler()
            #print(parenth)
    return len(parenth) == 0

print(valide("()"))
print(valide("[([bonjour+]essai)7plus- ];"))
print(valide("("))
print(valide(")("))
print(valide("4(essai]"))      
