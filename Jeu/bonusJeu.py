# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 15:08:31 2022

@author: rapha
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
        self.__sprite = ImageTk.PhotoImage((Image.open("Bonus.png")).resize((40,40), Image.ANTIALIAS))
        self.__display = self.__canevas.create_image(self._vaisseau__posX -20,self._vaisseau__posY-20, anchor=tk.NW, image=self.__sprite, tag = "bonus")
        
    def move(self):
        #print(self._vaisseau__posX, self.pos)
        if self._vaisseau__posX >=920:
            self.__canevas.delete(self.__display)
            self.__entities[3].remove(self)
            return(None)
        elif self._vaisseau__alive == False:
            self.__entities[0].get_ally()
            return(None)
        else:
            self._vaisseau__posX += 20
            self.__canevas.move("bonus", 20, 0)
        self.__canevas.after(200, self.move)
    
    def appear(self):
        self._vaisseau__posY = 100
        self.__sprite = ImageTk.PhotoImage((Image.open("Bonus.png")).resize((40,40), Image.ANTIALIAS))
        self.__display = self.__canevas.create_image(self._vaisseau__posX -20,self._vaisseau__posY-20, anchor=tk.NW, image=self.__sprite, tag = "bonus")
        self.move()
        
    def behavior(self):
        self.__canevas.after(randint(4000, 10000), self.appear)