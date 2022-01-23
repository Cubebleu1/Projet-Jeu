# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 15:08:30 2022

@author: rapha
"""
import tkinter as tk
from PIL import ImageTk, Image
from vaisseau import vaisseau
from mechantTire import mechantTire
from projectile import projectile
from random import randint

#Classe du boss final, très dur a vaincre :(      
class final_boss(vaisseau):
    def __init__(self, gui, couleur, posX, posY, tag, entities):
        super().__init__(gui, couleur, posX, posY, tag)
        self.__gui = gui
        self.__canevas = gui.get_canevas()
        self.stats = (40, 2, 5000)
        self.__entities=entities
        self._vaisseau__type="boss"
        self.__posX = self.pos[0]
        self.__posY = self.pos[1]
    
    def final_boss_sprite(self):
        self.__canevas.delete(self.get_sprite())
        self.__sprite = ImageTk.PhotoImage((Image.open("images/BossGalaga.png")).resize((200,200), Image.ANTIALIAS))
        self.__display = self.__canevas.create_image(self.__posX -20,self.__posY-20, anchor=tk.CENTER, tag="boss", image=self.__sprite)

        
    def super_shoot(self):    
        if self.is_alive == True :
            bullet1 = projectile(self.__gui, self.__posX -4, self.__posY, 2, 'orange', self.__entities)
            bullet1.routine()
            bullet2 = projectile(self.__gui, self.__posX - 30, self.__posY, 2, 'orange', self.__entities )
            bullet2.routine()
            self.__canevas.after(randint(1000, 2000), self.super_shoot)
        else:
            return(None)    
        
    def behavior(self):
        self.__canevas.after(2000, self.super_shoot)
