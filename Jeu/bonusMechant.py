# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 15:08:30 2022
Classe d'un méchant plus rare et plus puissant que les autres mais qui rapporte plus de points ! De base, l'idée était de faire en sorte que 
ce méchant donne un bonus léger au joueur si il était vaincu, mais par manque de temps nous n'avons pas pu implémenter cette
fonctionnalité.

TO DO LIST : 
    - Faire en sorte qui si l'ennemi est tué, il offre un bonus (défence, vitesse, ou vie (plus rare)), en utilisant choices du
    module random de la même manière que utilisé lors de la création d'enemis aléatoire dans la classe game !

@author: Raphaël CAUDRON & Arthur JEZEQUEL
"""
from mechantTire import mechantTire      
class bonusMechant(mechantTire):
    def __init__(self, canevas, couleur, posX, posY, tag, tout):
        super().__init__(canevas, couleur, posX, posY, tag, tout)
        self._vaisseau__type = "bonusmechant"
        self.stats = (4, 1, 100)
