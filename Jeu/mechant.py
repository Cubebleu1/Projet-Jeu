# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 15:08:30 2022

@author: rapha et arthu
"""
from vaisseau import vaisseau
#Mechant de base, il ne tire pas.
class mechant(vaisseau):
    def __init__(self, gui,couleur, POSX, POSY, tag):
        super().__init__(gui, couleur, POSX, POSY, tag)
        self._vaisseau__type = "normal"
        self.stats = (1, 1, 10)
        
    def behavior(self):
        pass
