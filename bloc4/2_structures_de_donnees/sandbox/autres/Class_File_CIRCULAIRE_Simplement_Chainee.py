# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 20:53:02 2020

@author: ruelr
"""


class Cellule:
    def __init__(self,value):
        self.value=value
        self.suivant=None
        
class File:
    
    def __init__(self):
        self.dernier=None
        self.longueur=0
    def vide(self):
        return self.longueur==0
    
    def ajout(self,x):
        c=Cellule(x)
        if self.vide():
            c.suivant=c
        else:
            c.suivant=self.dernier.suivant
            self.dernier.suivant=c
        self.dernier=c
        self.longueur+=1
            
            
    def defiler(self):
        if self.vide():
            raise ValueError("file vide")
        if self.dernier.suivant is self.dernier:
            c=self.dernier
            self.dernier=None
            self.longueur-=1
        else :
            c=self.dernier.suivant
            self.dernier.suivant=c.suivant
            self.longueur-=1
        return c.value
            
    def longueur(self):
        return self.longueur
    
tab=File()
tab.ajout(5)
tab.ajout(4)
tab.ajout(8)

print(tab.longueur)
     
    