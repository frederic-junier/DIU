# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 09:02:32 2020

@author: R
"""




class Cellule:
    def __init__(self,info,suivant):
        self.suivant=suivant
        self.info=info
        
class Liste:
    def __init__(self):
        self.premier=None
        
    def __str__(self):
        ch=''
        elt=self.premier
        while elt:
            ch+=str(elt.info)+" "
            elt=elt.suivant
        return "["+ch+"]"
        
        
        
    def estVide(self):
        return self.premier==None
    
    def Vider(self):
        while self.premier:
            self.premier=self.premier.suivant

            
    def nbElement(self):
        nb=0
        elt=self.premier
        while elt:
            nb+=1
            elt=elt.suivant
        return nb
    
    def ajouterEnTete(self,infoElement):
        self.premier=Cellule(infoElement, self.premier)
       
    def supprimerEnTete(self):
        elt=self.premier
        self.premier=elt.suivant
        del elt
        
    def traiter(self):
        elt=self.premier
        del self.premier
        print(self.premier)
        print(elt)
        self.premier=elt.suivant
        return elt.info
    
    def ajouterEnQueue(self,infoElement):
        if self.estVide():
            self.ajouterEnTete(infoElement)
        else:
            elt=self.premier
            while elt.suivant:
                elt=elt.suivant
            elt.suivant=Cellule(infoElement, None)
            
            
tab=Liste()
tab.ajouterEnTete(5)
tab.ajouterEnTete(10)
tab.ajouterEnTete(8)
tab.ajouterEnTete(4)

print(tab)