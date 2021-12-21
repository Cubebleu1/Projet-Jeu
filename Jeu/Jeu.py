#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 13:42:18 2021

@author: arthur.jezequel
"""
from tkinter import Tk, Frame, Label, Button, Canvas, Entry, Menu, PhotoImage, StringVar
import tkinter
import Fonctions_Jeu as fj
from PIL import ImageTk, Image



Mafenetre = Tk()
Mafenetre.title('Space  Invaders')

#Menu
MenuMain = Menu(Mafenetre)

MenuOptions = Menu(MenuMain, tearoff = 0)
MenuMain.add_cascade(label="Options", menu=MenuOptions)
MenuOptions.add_command(label = 'Controle', command = Mafenetre.destroy)
MenuOptions.add_command(label = 'PleinEcran', command = Mafenetre.destroy)

MenuGame = Menu(MenuMain, tearoff = 0)
MenuMain.add_cascade(label ="Modes de Jeu", menu=MenuGame)
MenuGame.add_command(label = 'Hardcore Mode', command = Mafenetre.destroy)
MenuGame.add_command(label = 'Easy Mode', command = Mafenetre.destroy)


Mafenetre.config(menu = MenuMain)

#Creation Canevas
image_background = ImageTk.PhotoImage(file = 'Background.png')
Canevas = Canvas(Mafenetre, width = 2*470, height = 2*320, bg ='darkblue')
Canevas.create_image(0,0, anchor=tkinter.NW, image = image_background)
Canevas.focus_set()
Canevas.pack(padx = 5, pady = 5)

#Bouton Quitter
ExitBtn = Button(Mafenetre, text = 'Quitter', command = Mafenetre.destroy)
ExitBtn.pack(side = 'left', padx = 5, pady = 5)

#Bouton Jouer
StartBtn = Button(Mafenetre, text = 'Jouer', command = Mafenetre.destroy)
StartBtn.pack(side = 'left', padx = 5, pady = 5)

#Bouton Reset
ResetBtn = Button(Mafenetre, text = 'Recommencer', command = Mafenetre.destroy)
ResetBtn.pack(side = 'left', padx = 5, pady = 5)

#Vies & Score
MainFrame = Frame(Mafenetre)
MainFrame.pack(side ='right')
Label(MainFrame, text='Score : 0').pack(side = 'right', padx = 10, pady = 10)
Label(MainFrame, text='Vies : 3').pack(side = 'right', padx = 10, pady = 10)

#Vaisseau Joueur
VaisseauJoueur = fj.vaisseau(Canevas, 'red',470,620)
Canevas.bind('<Key>', VaisseauJoueur.mvmt)

Alien = fj.mechant(Canevas, 'green', 100, 100)
Canevas.after(1000, Alien.clockmove)



Mafenetre.mainloop()