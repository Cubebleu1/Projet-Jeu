#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 13:42:18 2021
Page qui permet de lancer le jeu, tout simplement !

TO DO LIST :
    - Pas grand chose en soi, cette page n'est vraiment que là pour initier la création de l'interface utilisateur
    
@author: Raphaël CAUDRON & Arthur JEZEQUEL
"""
from tkinter import Tk
import gui as guint

ma_fenetre = Tk()
ma_fenetre.title('Space  Invaders') 

guint.GUI(ma_fenetre)


