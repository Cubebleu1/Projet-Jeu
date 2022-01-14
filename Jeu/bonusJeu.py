# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 15:08:31 2022

@author: rapha
"""
from vaisseau import vaisseau
#Classe d'une entité inofensive mais qui offre un bonus temporaire lorsque vaincu
class bonusJeu(vaisseau):
    def __init__(self):
        self.__img="alienBonus.jpg"
        self.__couleur="jaune"
    def meurt(self):
        return self.__genres
