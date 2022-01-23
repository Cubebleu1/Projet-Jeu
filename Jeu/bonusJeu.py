# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 15:08:31 2022
Cette classe est celle d'un bonus unique lors de la partie qui apparaît aléatoirement au cours de la partie, et qui raporte un 
super bonus : le joueur gagne un alié le temps du niveau

TO DO LIST :
    - Implémenter d'autres formes de supers bonus : invinsibilité temporaire (quelques secondes), tir en rafale, ....
    - Avoir plus d'un seul bonus par niveaux
    
@author: Raphaël CAUDRON & Arthur JEZEQUEL
"""
from vaisseau import vaisseau
from random import randint
import tkinter as tk
from PIL import ImageTk, Image
#Classe d'une entité inofensive mais qui offre un bonus temporaire lorsque vaincu
class bonusJeu(vaisseau):
    def __init__(self, gui, couleur, posX, posY, tag, entities):
        super().__init__(gui, couleur, posX, posY, tag)
        self.__entities = entities
        self.stats = (1, 1, 250)
        self._vaisseau__type="bonus"
        self.__gui = gui
        self.__canevas = self.__gui.get_canevas()
        
    #Le mouvement du bonus est unique ! Il va de gauche à droite rapidement et disparaît si il n'est pas tué.
    def move(self):
        #Si le bonus est hors du champ d'action, tant pis, il disparaît et le joueur n'a pas de bonus
        if self._vaisseau__posX >=920:
            self.__canevas.delete(self.__display)
            self.__entities[3].remove(self)
            return(None)
        #Si le bonus est vaincu, le joueur gagne un alié temporaire !
        elif self._vaisseau__alive == False:
            self.__entities[0].get_ally()
            return(None)
        #Sinon, le bonus continue sa trajectoire
        else:
            self._vaisseau__posX += 20
            self.__canevas.move("bonus", 20, 0)
        self.__canevas.after(200, self.move)
    
    
    #Cette fonction inite le comportement du bonus après qu'il soit apparu
    def appear(self):
        self._vaisseau__posY = 200
        self.__sprite = ImageTk.PhotoImage((Image.open("images/PinkAlien.png")).resize((40,40), Image.ANTIALIAS))
        self.__display = self.__canevas.create_image(self._vaisseau__posX -20,self._vaisseau__posY-20, anchor=tk.NW, image=self.__sprite, tag = "bonus")
        self.move()
        
    #le bonus ne devrait pas apparaître tout de suite, cette fonction permet de "retarder" son apparition sur le canevas        
    def behavior(self):
        self.__canevas.after(randint(4000, 14000), self.appear)