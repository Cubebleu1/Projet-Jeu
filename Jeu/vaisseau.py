# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 15:08:30 2022

@author: rapha
"""
import tkinter as tk
from PIL import ImageTk, Image

class vaisseau : ### ON PEUT VIRER COULEUR NON ?###
    def __init__(self,gui,couleur, posX, posY, tag):
        
        self.__alive = True
        self.__type = "None"
        self.__pv=0
        self.__dmg=0
        self.__gui = gui
        self.__canevas = gui.get_canevas()
        self.__tag = tag
        self.__couleur=couleur
        self.__points=0
        self.__posX = posX
        self.__posY = posY
        #self.__rectangle = self.__canevas.create_rectangle(self.__posX-20, self.__posY-20, self.__posX+20, self.__posY+20, tags = self.__tag, width ='1', outline =couleur)
        self.__sprite = ImageTk.PhotoImage((Image.open("images/PlayerSpaceShip.png")).resize((40,40), Image.ANTIALIAS))
        self.__display = self.__canevas.create_image(self.__posX -20,self.__posY-20, anchor=tk.NW, image=self.__sprite, tag = self.__tag)

    def follow(self, localisation):
        (direction, target_to_folow) = localisation
        (self.__posX, self.__posY) = target_to_folow.pos
        #self.__posX = target_to_folow[0]
        #self.__posY = target_to_folow[1]
        self.__canevas.coords(self.__display , self.__posX +73*direction, self.__posY -50)
        #canevas.coords(self.__rectangle , self.__posX -20, self.__posY -20, self.__posX +20, self.__posY +20)
        self.pos = (self.__posX +60*direction, self.__posY)
        self.__canevas.after(10, lambda : self.follow(localisation))
        #print(self.pos, "vue display")
        #sans lambda, la fonction follow est éxécutée en boucle sans fin et sans temporalisation (le .after n'a aucun effet)

    
    # --- Properties --- #
    def get_pos(self):
        return ([self.__posX, self.__posY])
    def set_pos(self, pos):
        (self.__posX, self.__posY) = pos       
    def del_pos(self):
        del self.__posX
        del self.__posY
    pos = property(get_pos, set_pos, del_pos, 'Position Property')
    
    def set_sprite(self, sprite_localisation):
        self.__canevas.delete(self.__display)
        self.__sprite = ImageTk.PhotoImage((Image.open(sprite_localisation)).resize((40,40), Image.ANTIALIAS))
        self.__display = self.__canevas.create_image(self.__posX -20,self.__posY-20, anchor=tk.NW, tag=self.__tag, image=self.__sprite)
    def get_sprite(self):
        return(self.__display)
    def del_sprite(self):
        del self.__display
    sprite = property(get_sprite, set_sprite, del_sprite, 'Sprite Property')
    
    def get_gui(self):
        return(self.__gui)
    
    def get_stats(self):
        return([self.__pv, self.__dmg, self.__points])
    def set_stats(self, new_stats):
        (self.__pv, self.__dmg, self.__points) = new_stats
    stats = property(get_stats, set_stats, None, 'Stats Property')
        
    
    def get_alive(self):
        return(self.__alive)
    def set_alive(self, Bool):
        self.__alive = Bool
    is_alive = property(get_alive, set_alive, None, 'Alive or not ?')
