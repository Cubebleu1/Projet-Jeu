#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 13:42:18 2021
Page qui permet de lancer le jeu, tout simplement !

TO DO LIST :
    - De manière générale, il faudrait revoir le code pour le rendre plus épuré. En effet, tout au long du projet, on a trouvé
    différentes méthodes pour gérer les attributs privés (changement de nomenclatures, utilisation de properties avec les GETTER
    ou SETTER, ...) ce qui peut rendre le code un peu brouillon. Cepedant, étant donné que c'est la première fois que l'on fait ça, 
    nous sommes quand même contents du résultat final ! Mais il reste bien sûr beaucoup de zones à améliorer.
    
@author: Raphaël CAUDRON & Arthur JEZEQUEL
"""
from tkinter import Tk
import gui as guint

ma_fenetre = Tk()
ma_fenetre.title('Space  Invaders') 

guint.GUI(ma_fenetre)


