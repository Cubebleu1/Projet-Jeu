#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 13:42:18 2021
 
@author: arthur.jezequel
"""
from tkinter import Tk, Frame, Label, Button, Canvas, Entry, Menu, PhotoImage, StringVar
#import tkinter
import Fonctions_Jeu as fj
#from PIL import ImageTk, Image 

 

ma_fenetre = Tk()
ma_fenetre.title('Space  Invaders')

fj.GUI(ma_fenetre)


"""
#Menu
menu_main = Menu(ma_fenetre)

menu_options = Menu(menu_main, tearoff = 0)
menu_main.add_cascade(label="Options", menu=menu_options)
menu_options.add_command(label = 'Controle', command = ma_fenetre.destroy)
menu_options.add_command(label = 'PleinEcran', command = ma_fenetre.destroy)

menu_game = Menu(menu_main, tearoff = 0)
menu_main.add_cascade(label ="Modes de Jeu", menu=menu_game)
menu_game.add_command(label = 'Hardcore Mode', command = ma_fenetre.destroy)
menu_game.add_command(label = 'Easy Mode', command = ma_fenetre.destroy)


ma_fenetre.config(menu = menu_main)

#Creation Canevas
image_background = ImageTk.PhotoImage(file = 'Background.png')
canevas = Canvas(ma_fenetre, width = 2*470, height = 2*320, bg ='darkblue')
canevas.create_image(0,0, anchor=tkinter.NW, image = image_background)
canevas.focus_set()
canevas.pack(padx = 5, pady = 5)

space_invaders = fj.game(canevas)

#Bouton Quitter
ExitBtn = Button(ma_fenetre, text = 'Quitter', command = ma_fenetre.destroy)
ExitBtn.pack(side = 'left', padx = 5, pady = 5)

#Bouton Jouer
StartBtn = Button(ma_fenetre, text = 'Jouer', command = lambda: fj.jeu(space_invaders, canevas, "NM"))

#StartBtn = Button(ma_fenetre, text = 'Jouer', command = ma_fenetre.destroy)
StartBtn.pack(side = 'left', padx = 5, pady = 5)

#Bouton Reset
ResetBtn = Button(ma_fenetre, text = 'Recommencer', command = lambda : fj.restart(space_invaders, canevas, "NM"))
ResetBtn.pack(side = 'left', padx = 5, pady = 5)

#Vies & Score
main_frame = Frame(ma_fenetre)
main_frame.pack(side ='right')
Label(main_frame, text='Score : 0').pack(side = 'right', padx = 10, pady = 10)
Label(main_frame, text='Vies : 3').pack(side = 'right', padx = 10, pady = 10)
"""
#Vaisseau Joueur
#VaisseauJoueur = fj.vaisseau(Canevas, 'red',470,620)
#Canevas.bind('<Key>', VaisseauJoueur.mvmt)

#test mechants
#Alien = fj.mechant(Canevas, 'green', 100, 100)
#AlienTire = fj.mechantTire(Canevas, 'red', 200, 200, VaisseauJoueur)
#Canevas.after(1000, fj.Jeu(Canevas, 'NM'))

"""
ma_fenetre.mainloop()"""