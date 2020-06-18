#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      CLAIRE_MARIE
#
# Created:     17/06/2020
# Copyright:   (c) CLAIRE_MARIE 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

class Pile :
    def __init__(self,L):
        self.liste=L

    def __repr__(self) :
        s='pile : '
        for e in self.liste:
            s+=str(e) + ''
        return s

    def empiler(self,e) :
        self.liste.insert(0,e)

    def depiler(self) :
        del self.liste[0]

    def sommet(self) :
        return self.liste[0]

    def estVide(self) :
        return len(self.liste)==0

    def hauteur(self) :
        return len(self.liste)

    def traiter(self) :
        e=self.liste[0]
        del self.liste[0]
        return e

class File :
    def __init__(self,L) :
        self.liste=L

    def __repr__(self) :
        s='File'
        for e in self.liste:
            s+= str(e) +' '
        return s

    def traiter(self) :
        e=self.liste[-1]
        del self.liste[-1]
        return e

    def enfiler(self,e) :
        self.liste.insert(0,e)

    def estVide(self) :
        return len(self.liste)==0

    def longueur(self):
        return len(self.liste)


def InverserFile(file) :
    pile=Pile()
    while not file.estVide():
        pile.empiler(file.traiter())
    while not pile.estVide():
        file.enfiler(pile.traiter())


def valide (ch):
    pile=Pile([])
    for car in ch:
        if car=='(' or car=='[' :
            pile.empiler(car)
        elif car==')':
            if not pile.estVide():
                sommet=pile.traiter()
                if sommet !='(':
                    return False
            else :
                return False
        elif car==']':
            if not pile.estVide():
                sommet=pile.traiter()
                if sommet !=('['):
                    return False
            else :
                return False

    return pile.estVide()

L = [0]
pile = Pile(L)
print("Ajout de 5 2 4 : ", end='')
pile.empiler(5)
pile.empiler(2)
pile.empiler(4)
print(pile)

#print(str('d'))

L = [0]
file = File(L)
print("Ajout en queue de 5 2 4 : ", end='')
file.enfiler(5)
file.enfiler(2)
file.enfiler(4)
print(file)

#InverserFile(12345)
#print(file)

print(valide('t(x'))














