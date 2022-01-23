# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 15:08:31 2022
Cette classe est celle des protections qui apparaissent à chaque niveau. Elles se brisent à chaque fois qu'elles subissent
4 dégats, jusqu'à ce briser. Il n'y a aucun moyen de les récupérer avant le niveau suivant.

TO DO LIST :
    - Les rendre plus jolies...
    
@author: Raphaël CAUDRON & Arthur JEZEQUEL
"""
from collections import deque
import tkinter as tk
from PIL import ImageTk, Image

#Ilot Protecteurs
class ilot:
    def __init__(self, gui, game, entities, posX, posY):
        self.__img="obstacle2"
        self.__pv=16
        self.__gui = gui
        self.__game = game
        self.__canevas = gui.get_canevas()
        self.__entities = entities
        self.__posX = posX
        self.__posY = posY
        self.__sprites = deque(["BlockStone/frame03.png", "BlockStone/frame02.png","BlockStone/frame01.png"])
        self.__rectangle = self.__canevas.create_rectangle(self.__posX-100, self.__posY-24, self.__posX+100, self.__posY+24, tags="protec", width ='1', outline ="grey", fill="grey")
        

    def get_stat(self):
        return(self.__pv)
    def set_stat(self, pv):
        self.__pv = pv
    def del_stat(self):
        del self.__pv
    stats = property(get_stat, set_stat, del_stat, 'Stat property')
    
    def get_pos(self):
        return ([self.__posX, self.__posY])
    def set_pos(self, pos):
        (self.__posX, self.__posY) = pos       
    def del_pos(self):
        del self.__posX
        del self.__posY
    pos = property(get_pos, set_pos, del_pos, 'Position Property')
    
    def sprites(self):
        self.__pv -= 1
        if self.__pv == 12 or self.__pv==8 or self.__pv==4:
            new_sprite=self.__sprites.popleft()
            self.__canevas.delete(self.__rectangle)
            self.__sprite = ImageTk.PhotoImage((Image.open(new_sprite)).resize((200,48), Image.ANTIALIAS))
            self.__display = self.__canevas.create_image(self.__posX -100,self.__posY-24, anchor=tk.NW, tag="protec", image=self.__sprite)
        if self.__pv == 0:
            self.__canevas.delete(self.__display)
            self.__entities[2].remove(self)
        