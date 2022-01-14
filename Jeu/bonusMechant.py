# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 15:08:30 2022

@author: rapha
"""
from mechantTire import mechantTire
#Classe d'un méchant rapide qui offre un super bonus si vaincu       
class bonusMechant(mechantTire):
    def __init__(self, canevas, couleur, posX, posY, tag, player, tout):
        super().__init__(canevas, couleur, posX, posY, tag, player, tout)
        self.__img="alienViolet.jpg"
        self.stats = (4, 1, 50)
        self.__points=150
