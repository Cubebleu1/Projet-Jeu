# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 15:08:30 2022

@author: rapha et arthu
"""
from vaisseau import vaisseau
from random import randint
from projectile import projectile
#Mechant qui peut tirer et blesser le joueur.      
class mechantTire(vaisseau):
    def __init__(self, gui,couleur, posX, posY, tag, entities):
        super().__init__(gui, couleur, posX, posY, tag)
        self.stats = (2, 1, 25)
        #self.__tirer=True
        self.__projectileC = gui.get_canevas()
        self.__entities = entities
    def shoot(self):
        if self.is_alive == True :
            bullet = projectile(self._vaisseau__gui, self._vaisseau__posX, self._vaisseau__posY, 0, 'yellow', self.__entities)
            bullet.routine()
            self.__projectileC.after(randint(2000, 6000), self.shoot)
        else:
            return(None)
    
    def behavior(self):
        self.__projectileC.after(randint(1000, 5000), self.shoot)
