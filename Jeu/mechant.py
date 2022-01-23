# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 15:08:30 2022
Classe d'un enemi classique, qui ne tire pas

TO DO LIST :
    - Rien de spécial
    
@author: Raphaël CAUDRON & Arthur JEZEQUEL
"""
from vaisseau import vaisseau
class mechant(vaisseau):
    def __init__(self, gui,couleur, POSX, POSY, tag):
        super().__init__(gui, couleur, POSX, POSY, tag)
        self._vaisseau__type = "normal"
        self.stats = (1, 1, 10)
        
    def behavior(self):
        #Cet ennemi n'a pas de comportement, il ne fait que se déplacer.
        pass
