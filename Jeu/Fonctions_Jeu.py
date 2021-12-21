#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 13:43:08 2021

@author: arthur.jezequel
"""
#import Jeu
import time;

class vaisseau : 
    def __init__(self,canevas,couleur, POSX, POSY):
        self.__pv=1
        self.__tirer=False
        self.__canevas = canevas
        self.__couleur=couleur
        self.__points=0
        self.__posX = POSX
        self.__posY = POSY
        self.__rectangle = self.__canevas.create_rectangle(self.__posX-20, self.__posY-20, self.__posX+20, self.__posY+20, width ='1', outline =couleur)
    
    def mvmt(self,event):
        if event.keysym == 'Right':
            self.__posX += 10
            self.__canevas.coords(self.__rectangle , self.__posX -20, self.__posY -20, self.__posX +20, self.__posY +20)
        if event.keysym == 'Left':
            self.__posX -= 10
            self.__canevas.coords(self.__rectangle , self.__posX -20, self.__posY -20, self.__posX +20, self.__posY +20)
            
    def meurt(self):
        self.__pv = 0
        return self.__points
    
    def touche(self,dmg):
        if self.__pv>0:
            self.__pv -= dmg
        else:
            vaisseau.meurt()   
    
    def deplacementlimite(self):
        if self.__posX > 940 or self.__posY > 620:
            print('stop')
            
    def clockmove(self):
        i = 0;
        while i<3:
            i = i +1
            time.sleep(2)
            self.__posX += 10
            self.__canevas.coords(self.__rectangle , self.__posX -20, self.__posY -20, self.__posX +20, self.__posY +20)
                
    
    
    
#Joueur
    
    
class joueur(vaisseau):
    def __init__(self,difficulte):
        self.__img="joueur.jpg"
        self.__tirer=True
        self.__couleur="bleu"
        self.__difficulte=difficulte
        self.__dmg=1
        self.__vitesse=5
    def pdv(self):
        if joueur.difficulte == "NM":
            self.__pv = 3
        elif joueur.difficulte == "HCM":
            self.__pv = 1
        else:
            self.__pv = 999
    
    def bonus(self,genre):
       if genre == "pv":
           self.__pv+=1
       elif genre == "dmg":
           self.__dmg+=1
            
            
#différents aliens 
class mechant(vaisseau):
    def __init__(self, canevas,couleur, POSX, POSY):
        super().__init__(canevas, couleur, POSX, POSY)
        self.__img="alienNoir.jpg"
        self.__points=10

        
class mechantTire(vaisseau):
    def __init__(self):
        self.__img="alienRouge.jpg"
        self.__tirer=True
        self.__points =25
        
class bonusMechant(mechantTire):
    def __init__(self):
        self.__img="alienViolet.jpg"
        self.__points=150
        
        
#Vaisseau bonus
class bonusJeu(vaisseau):
    def __init__(self):
        self.__img="alienBonus.jpg"
        self.__couleur="jaune"
    def meurt(self):
        return self.__genre
    
    
#Ilot Protecteurs
class ilot(vaisseau):
    def __init__(self,grosseur):
        self.__img="obstacle2"
        self.__pv=4
        self.__grosseur=grosseur
        
    

        
        
        